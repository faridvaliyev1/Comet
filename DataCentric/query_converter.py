from pathlib import Path
import argparse
import re

from Service.RDFWidePropertyTable import RDFWidePropertyTable
from Service.SparqlWorkload import SparqlWorkload
from Utils.DBContext import DbContext


DEFAULT_INPUT = Path("Queries/SPARQL/watdiv")
DEFAULT_OUTPUT_ROOT = Path("Queries/SQL")


class UnsupportedQueryError(Exception):
    pass


def quote_identifier(identifier):
    return '"' + identifier.replace('"', '""') + '"'


def sql_literal(value):
    return "'" + value.replace("'", "''") + "'"


def sparql_constant_value(token):
    token = token.strip()

    if token.startswith("<") and token.endswith(">"):
        return token[1:-1]

    if token.startswith('"'):
        match = re.match(r'"((?:\\.|[^"])*)"', token)
        if match:
            return match.group(1).replace('\\"', '"')

    return token


def read_sql_wpt_queries(path):
    text = path.read_text()

    if "--END--" in text:
        queries = [query.strip() for query in text.split("--END--")]
    else:
        queries = [
            query.strip()
            for query in re.split(r"(?m)^---\s*$", text)
        ]

    return [
        query
        for query in queries
        if query and query != "???" and "WPT" in query
    ]


def find_wpt_aliases(query):
    return re.findall(r"\b(?:FROM|JOIN)\s+WPT\s+([A-Za-z_][A-Za-z0-9_]*)", query, re.IGNORECASE)


def find_alias_columns(alias, query):
    columns = ["Subject"]

    for match in re.finditer(rf"\b{re.escape(alias)}\.([A-Za-z0-9_]+)", query):
        column = match.group(1)

        if column not in columns:
            columns.append(column)

    return columns


def find_table_columns(table):
    rows = DbContext.Select(
        f"SELECT column_name FROM global_mapping WHERE table_name = '{table}'"
    )

    return [row[0] for row in rows]


def find_candidate_tables(columns):
    rows = DbContext.Select(
        f"""
        SELECT DISTINCT table_name
        FROM global_mapping
        WHERE column_name IN {tuple(columns)}
        """
    )

    return [row[0] for row in rows]


def choose_tables(columns):
    remaining_columns = set(columns)
    remaining_columns.discard("Subject")
    candidate_tables = find_candidate_tables(columns)
    selected_tables = []

    table_columns = {
        table: set(find_table_columns(table))
        for table in candidate_tables
    }

    while remaining_columns:
        best_table = None
        best_overlap = set()

        for table, columns_in_table in table_columns.items():
            overlap = columns_in_table.intersection(remaining_columns)

            if len(overlap) > len(best_overlap):
                best_table = table
                best_overlap = overlap

        if best_table is None:
            missing_columns = ", ".join(sorted(remaining_columns))
            raise RuntimeError(f"No generated table found for columns: {missing_columns}")

        selected_tables.append(best_table)
        remaining_columns -= best_overlap

    return selected_tables


def table_for_column(tables, column):
    return next(table for table in tables if column in find_table_columns(table))


def build_wpt_replacement(alias, columns):
    tables = choose_tables(columns)
    first_table = tables[0]

    select_columns = [
        f"{first_table}.{quote_identifier('Subject')} AS {quote_identifier('Subject')}"
    ]

    for column in columns:
        if column == "Subject":
            continue

        source_table = table_for_column(tables, column)
        select_columns.append(
            f"{source_table}.{quote_identifier(column)} AS {quote_identifier(column)}"
        )

    return build_subquery(alias, tables, select_columns)


def build_subquery(alias, tables, select_columns):
    first_table = tables[0]
    join_sql = first_table

    for table in tables[1:]:
        join_sql += (
            f"\nFULL JOIN {table}"
            f" ON {table}.{quote_identifier('Subject')} = "
            f"{first_table}.{quote_identifier('Subject')}"
        )

    return (
        "(SELECT "
        + ", ".join(select_columns)
        + "\nFROM "
        + join_sql
        + f") AS {alias}"
    )


def quote_alias_references(query, aliases):
    for alias in aliases:
        query = re.sub(
            rf"\b{re.escape(alias)}\.([A-Za-z0-9_]+)",
            lambda match: f"{alias}.{quote_identifier(match.group(1))}",
            query,
        )

    return query


def convert_sql_wpt_query(query):
    aliases = find_wpt_aliases(query)
    converted = query

    for alias in aliases:
        columns = find_alias_columns(alias, query)
        replacement = build_wpt_replacement(alias, columns)
        converted = re.sub(
            rf"\bWPT\s+{re.escape(alias)}\b",
            replacement,
            converted,
            flags=re.IGNORECASE,
        )

    return quote_alias_references(converted, aliases)


def is_variable(token):
    return token.startswith("?")


def alias_for_subject(subject, index):
    if is_variable(subject):
        return "T_" + subject[1:]

    return "T_const_" + str(index)


def convert_sparql_query(query, workload):
    all_triples = workload.triple_patterns(query)
    triples = [triple for triple in all_triples if not triple[1].startswith("?")]

    if len(triples) == 0:
        raise UnsupportedQueryError("queries with only variable predicates are not supported")

    selected_variables = workload.selected_variables(query)
    groups = {}
    variable_sources = {}
    where_conditions = []

    for index, (subject, predicate, obj) in enumerate(triples):
        alias = alias_for_subject(subject, index)
        column = RDFWidePropertyTable.normalize_uri(predicate)
        groups.setdefault(alias, {"subject": subject, "columns": ["Subject"], "triples": []})

        if column not in groups[alias]["columns"]:
            groups[alias]["columns"].append(column)

        groups[alias]["triples"].append((subject, column, obj))

        if is_variable(subject):
            variable_sources.setdefault(subject, []).append((alias, "Subject"))

        if is_variable(obj):
            variable_sources.setdefault(obj, []).append((alias, column))

    from_parts = []

    for alias, group in groups.items():
        tables = choose_tables(group["columns"])
        first_table = tables[0]
        select_columns = [
            f"{first_table}.{quote_identifier('Subject')} AS {quote_identifier('Subject')}"
        ]

        for column in group["columns"]:
            if column == "Subject":
                continue

            source_table = table_for_column(tables, column)
            select_columns.append(
                f"{source_table}.{quote_identifier(column)} AS {quote_identifier(column)}"
            )

        from_parts.append(build_subquery(alias, tables, select_columns))

        subject = group["subject"]
        if not is_variable(subject):
            where_conditions.append(
                f"{alias}.{quote_identifier('Subject')} = {sql_literal(sparql_constant_value(subject))}"
            )

        for _subject, column, obj in group["triples"]:
            if is_variable(obj):
                where_conditions.append(
                    f"{alias}.{quote_identifier(column)} IS NOT NULL"
                )
                continue

            where_conditions.append(
                f"{alias}.{quote_identifier(column)} = {sql_literal(sparql_constant_value(obj))}"
            )

    for variable, sources in variable_sources.items():
        first_alias, first_column = sources[0]

        for alias, column in sources[1:]:
            if alias == first_alias and column == first_column:
                continue

            where_conditions.append(
                f"{first_alias}.{quote_identifier(first_column)} = "
                f"{alias}.{quote_identifier(column)}"
            )

    select_columns = []

    for variable in selected_variables:
        sources = variable_sources.get(variable)

        if sources is None:
            continue

        alias, column = sources[0]
        select_columns.append(
            f"{alias}.{quote_identifier(column)} AS {quote_identifier(variable[1:])}"
        )

    if len(select_columns) == 0:
        select_columns.append("*")

    sql = "SELECT DISTINCT " + ", ".join(select_columns)

    if len(from_parts) == 0:
        raise UnsupportedQueryError("no concrete triple patterns found")

    sql += "\nFROM " + "\nCROSS JOIN ".join(from_parts)

    if where_conditions:
        sql += "\nWHERE " + "\nAND ".join(where_conditions)

    return sql


def default_sql_output_path(input_path, dataset_name=None):
    input_path = Path(input_path)

    if dataset_name:
        return DEFAULT_OUTPUT_ROOT / dataset_name

    if input_path.is_dir():
        return DEFAULT_OUTPUT_ROOT / input_path.name

    if input_path.suffix == ".sparql":
        return DEFAULT_OUTPUT_ROOT / input_path.parent.name / f"{input_path.stem}.sql"

    return Path("Queries/converted.txt")


def write_sparql_conversions(input_path, output_path=None, dataset_name=None):
    input_path = Path(input_path)
    output_path = Path(output_path) if output_path else default_sql_output_path(input_path, dataset_name)
    workload = SparqlWorkload(input_path)
    converted_count = 0

    if input_path.is_dir():
        output_path.mkdir(parents=True, exist_ok=True)

        for path, query in workload.read_queries():
            try:
                converted = convert_sparql_query(query, workload)
            except (UnsupportedQueryError, RuntimeError) as exc:
                converted = f"-- Unsupported query: {path.name}: {exc}"

            (output_path / f"{path.stem}.sql").write_text(converted + "\n")
            converted_count += 1

        return converted_count, output_path

    if output_path.suffix != ".sql":
        output_path.mkdir(parents=True, exist_ok=True)
        output_file = output_path / f"{input_path.stem}.sql"
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_file = output_path

    path, query = workload.read_queries()[0]

    try:
        converted = convert_sparql_query(query, workload)
    except (UnsupportedQueryError, RuntimeError) as exc:
        converted = f"-- Unsupported query: {path.name}: {exc}"

    output_file.write_text(converted + "\n")
    return 1, output_file


def write_wpt_sql_conversions(input_path, output_path=None):
    input_path = Path(input_path)
    output_path = Path(output_path) if output_path else default_sql_output_path(input_path)
    converted_queries = [
        convert_sql_wpt_query(query)
        for query in read_sql_wpt_queries(input_path)
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n---\n".join(converted_queries) + "\n")

    return len(converted_queries), output_path


def convert_workload(input_path, output_path=None, dataset_name=None):
    input_path = Path(input_path)

    if input_path.is_dir() or input_path.suffix == ".sparql":
        return write_sparql_conversions(input_path, output_path, dataset_name)

    return write_wpt_sql_conversions(input_path, output_path)


def main():
    parser = argparse.ArgumentParser(description="Convert a SPARQL or WPT-SQL workload to SQL over generated tables.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="SPARQL file/folder or WPT-SQL workload file")
    parser.add_argument("--output", default=None, help="Output .sql file for one query, or output directory for a SPARQL folder")
    parser.add_argument("--dataset-name", default=None, help="Dataset folder name under Queries/SQL")
    args = parser.parse_args()

    count, output_path = convert_workload(args.input, args.output, args.dataset_name)

    print(f"Converted {count} query/query block(s)")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
