# DataCentric RDF Schema Generation

This project builds a data-centric relational schema from an RDF dataset and a SPARQL query workload.

The pipeline:

1. Reads an RDF dataset in `.nt` or line-oriented `.n3` format.
2. Generates a wide property table (WPT) CSV.
3. Imports the WPT into PostgreSQL as `wpt_tbl`.
4. Runs the existing metrics, clustering, partitioning, star-pattern, and mapping logic.
5. Creates generated relational tables named `tables_*`.
6. Exports those tables to CSV.
7. Converts the SPARQL workload into SQL over the generated schema.

## Project Layout

```text
Data/
  watdiv/watdiv.nt
  sp2bench/sp2b.n3
  generated/
  results/h2o/

Queries/
  SPARQL/
    watdiv/*.sparql
    sp2bench/*.sparql
  SQL/
    watdiv/*.sql
    sp2bench/*.sql

Service/
  RDFWidePropertyTable.py
  SparqlWorkload.py
  StarPattern.py
  Mapping.py

main.py
query_converter.py
Configurations.py
```

## Requirements

Install the Python dependencies in your virtual environment:

```bash
pip install -r requirements.txt
```

PostgreSQL must be running and match the connection settings in `Configurations.py`:

```python
DATABASE_NAME = "comet_db"
DATABASE_USER = "comet_user"
DATABASE_PASSWORD = "comet"
DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"
```

## Running The Full Pipeline

WatDiv:

```bash
python main.py \
  --dataset Data/watdiv/watdiv.nt \
  --workload Queries/SPARQL/watdiv \
  --dataset-name watdiv
```

SP2Bench:

```bash
python main.py \
  --dataset Data/sp2bench/sp2b.n3 \
  --rdf-format n3 \
  --workload Queries/SPARQL/sp2bench \
  --dataset-name sp2bench
```

By default, converted SQL queries are written as one file per SPARQL query:

```text
Queries/SQL/<dataset-name>/<query-name>.sql
```

For example:

```text
Queries/SQL/watdiv/C1.sql
Queries/SQL/sp2bench/q1.sql
```

## Useful Arguments

```text
--dataset           RDF dataset path, usually .nt or .n3
--rdf-format        Optional format override: nt or n3
--workload          SPARQL workload file or directory
--dataset-name      Name used for Queries/SQL/<dataset-name>
--wpt-output        Optional generated WPT CSV path
--converted-output  Optional converted SQL output directory
--support-threshold Existing clustering support threshold
--null-threshold    Existing partitioning null threshold
```

Example with explicit output paths:

```bash
python main.py \
  --dataset Data/watdiv/watdiv.nt \
  --workload Queries/SPARQL/watdiv \
  --dataset-name watdiv \
  --wpt-output Data/generated/wpt_watdiv.csv \
  --converted-output Queries/SQL/watdiv
```

## Converting Queries Only

After a generated schema and `GLOBAL_MAPPING` exist in PostgreSQL, you can convert a workload without rerunning the full pipeline.

```bash
python query_converter.py --input Queries/SPARQL/watdiv
python query_converter.py --input Queries/SPARQL/sp2bench
```

You can override the output location:

```bash
python query_converter.py \
  --input Queries/SPARQL/watdiv \
  --output Queries/SQL/custom-watdiv
```

## Notes

- `query_converter.py` depends on the current `GLOBAL_MAPPING` table, so run it against the same dataset schema that produced that mapping.
- SPARQL queries with only variable predicates are marked as unsupported in their `.sql` output file.
- The RDF parser is intentionally dependency-free and targets the line-oriented benchmark files in this repository.
