from pathlib import Path
import re

from Service.RDFWidePropertyTable import RDFWidePropertyTable


class SparqlWorkload:
    def __init__(self, workload_path):
        self.workload_path = Path(workload_path)

    def files(self):
        if self.workload_path.is_dir():
            return sorted(self.workload_path.glob("*.sparql"))

        return [self.workload_path]

    def read_queries(self):
        queries = []

        for path in self.files():
            text = path.read_text()

            if "--END--" in text:
                blocks = text.split("--END--")
            elif re.search(r"(?m)^---\s*$", text):
                blocks = re.split(r"(?m)^---\s*$", text)
            else:
                blocks = [text]

            for block in blocks:
                query = block.strip()

                if query and query != "???":
                    queries.append((path, query))

        return queries

    @staticmethod
    def parse_prefixes(query):
        prefixes = {}

        for line in query.splitlines():
            line = line.strip()

            if line.upper().startswith("PREFIX"):
                parts = line.split()
                if len(parts) >= 3:
                    prefixes[parts[1]] = parts[2].strip("<>")

        return prefixes

    @staticmethod
    def expand_token(token, prefixes):
        token = token.strip()

        if token.startswith("<") and token.endswith(">"):
            return token[1:-1]

        if token.startswith("?") or token.startswith('"') or token.startswith("_:"):
            return token

        if ":" in token and not token.startswith(("http://", "https://")):
            prefix, name = token.split(":", 1)
            prefix_key = prefix + ":"

            if prefix_key in prefixes:
                return prefixes[prefix_key] + name

        return token

    @staticmethod
    def split_statements(text):
        statements = []
        token = []
        in_quote = False
        in_angle = False
        escape = False

        for char in text:
            if escape:
                token.append(char)
                escape = False
                continue

            if char == "\\" and in_quote:
                token.append(char)
                escape = True
                continue

            if char == '"' and not in_angle:
                in_quote = not in_quote
                token.append(char)
                continue

            if char == "<" and not in_quote:
                in_angle = True
                token.append(char)
                continue

            if char == ">" and not in_quote:
                in_angle = False
                token.append(char)
                continue

            if char == "." and not in_quote and not in_angle:
                statement = "".join(token).strip()
                if statement:
                    statements.append(statement)
                token = []
                continue

            token.append(char)

        statement = "".join(token).strip()
        if statement:
            statements.append(statement)

        return statements

    @staticmethod
    def tokenize_statement(statement):
        return RDFWidePropertyTable.tokenize_statement(statement)

    @staticmethod
    def where_body(query):
        start = query.find("{")
        end = query.rfind("}")

        if start < 0 or end < 0 or end <= start:
            return ""

        return query[start + 1:end]

    @staticmethod
    def filter_predicate_bindings(body, prefixes):
        bindings = {}

        for left, right in re.findall(r"FILTER\s*\(\s*(\?[A-Za-z0-9_]+)\s*=\s*([^)]+?)\s*\)", body, re.IGNORECASE):
            bindings[left] = SparqlWorkload.expand_token(right.strip(), prefixes)

        return bindings

    @staticmethod
    def selected_variables(query):
        match = re.search(r"SELECT\s+(.*?)\s+WHERE", query, re.IGNORECASE | re.DOTALL)

        if not match:
            return []

        return re.findall(r"\?[A-Za-z0-9_]+", match.group(1))

    def triple_patterns(self, query):
        prefixes = self.parse_prefixes(query)
        body = self.where_body(query)
        predicate_bindings = self.filter_predicate_bindings(body, prefixes)
        triples = []
        in_filter = False
        statement = []

        for line in body.splitlines():
            current_line = line.strip()

            if not current_line:
                continue

            upper_statement = current_line.upper()

            if in_filter:
                if ")" in current_line:
                    in_filter = False
                continue

            if "FILTER" in upper_statement:
                if ")" not in current_line:
                    in_filter = True
                continue

            if upper_statement.startswith("OPTIONAL") or upper_statement.startswith("UNION") or current_line in ("{", "}") or current_line.startswith("}"):
                if statement:
                    triples.extend(self.triples_from_statement(" ".join(statement), prefixes, predicate_bindings))
                    statement = []
                continue

            statement.append(current_line)

            if current_line.endswith("."):
                triples.extend(self.triples_from_statement(" ".join(statement), prefixes, predicate_bindings))
                statement = []

        if statement:
            triples.extend(self.triples_from_statement(" ".join(statement), prefixes, predicate_bindings))

        return triples

    def triples_from_statement(self, statement, prefixes, predicate_bindings):
        statement = statement.strip()

        if statement.endswith("."):
            statement = statement[:-1].strip()

        tokens = self.tokenize_statement(statement)

        if len(tokens) < 3:
            return []

        subject = self.expand_token(tokens[0], prefixes)
        triples = []
        index = 1

        while index < len(tokens):
            if tokens[index] in (";", ","):
                index += 1
                continue

            predicate = self.expand_token(tokens[index], prefixes)
            index += 1
            object_tokens = []

            while index < len(tokens) and tokens[index] not in (";", ","):
                object_tokens.append(tokens[index])
                index += 1

            if not object_tokens:
                continue

            if predicate in predicate_bindings:
                predicate = predicate_bindings[predicate]

            obj = self.expand_token(" ".join(object_tokens), prefixes)
            triples.append((subject, predicate, obj))

        return triples
