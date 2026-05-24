from collections import defaultdict
import csv
from pathlib import Path


class RDFWidePropertyTable:
    def __init__(self, dataset_path, output_path=None, rdf_format=None):
        self.dataset_path = Path(dataset_path)
        self.rdf_format = rdf_format or self.dataset_path.suffix.lower().lstrip(".")
        self.output_path = Path(output_path) if output_path else self.default_output_path()
        self.prefixes = {}

    def default_output_path(self):
        return Path("Data/generated") / f"wpt_{self.dataset_path.stem}.csv"

    @staticmethod
    def normalize_uri(uri):
        return "".join(c if c.isalnum() else "_" for c in uri).strip("_")

    def expand_token(self, token):
        token = token.strip()

        if token.startswith("<") and token.endswith(">"):
            return token[1:-1]

        if token.startswith("_:"):
            return token

        if ":" in token and not token.startswith(("http://", "https://")):
            prefix, name = token.split(":", 1)
            prefix_key = prefix + ":"

            if prefix_key in self.prefixes:
                return self.prefixes[prefix_key] + name

        return token

    def parse_prefix(self, line):
        line = line.strip()

        if line.lower().startswith("@prefix"):
            parts = line.split()
            if len(parts) >= 3:
                self.prefixes[parts[1]] = parts[2].strip("<>")
            return True

        if line.upper().startswith("PREFIX"):
            parts = line.split()
            if len(parts) >= 3:
                self.prefixes[parts[1]] = parts[2].strip("<>")
            return True

        return False

    @staticmethod
    def tokenize_statement(statement):
        tokens = []
        token = []
        in_quote = False
        in_angle = False
        escape = False

        for char in statement.strip():
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

            if char.isspace() and not in_quote and not in_angle:
                if token:
                    tokens.append("".join(token))
                    token = []
                continue

            token.append(char)

        if token:
            tokens.append("".join(token))

        return tokens

    def parse_triple(self, line):
        line = line.strip()

        if not line or line.startswith("#") or self.parse_prefix(line):
            return None

        if line.endswith("."):
            line = line[:-1].strip()

        tokens = self.tokenize_statement(line)

        if len(tokens) < 3:
            return None

        subject = self.expand_token(tokens[0])
        predicate = self.expand_token(tokens[1])
        obj = self.expand_token(" ".join(tokens[2:]))

        return subject, predicate, obj

    def generate(self):
        rows = defaultdict(lambda: defaultdict(list))
        predicates = []
        seen_predicates = set()

        with self.dataset_path.open() as file:
            for line in file:
                triple = self.parse_triple(line)

                if triple is None:
                    continue

                subject, predicate, obj = triple
                column = self.normalize_uri(predicate)

                if column not in seen_predicates:
                    seen_predicates.add(column)
                    predicates.append(column)

                rows[subject][column].append(obj)

        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with self.output_path.open("w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Subject"] + predicates)

            for subject, values in rows.items():
                csv_row = [subject]

                for predicate in predicates:
                    objects = values.get(predicate, [])

                    if len(objects) == 0:
                        csv_row.append("")
                    elif len(objects) == 1:
                        csv_row.append(objects[0])
                    else:
                        csv_row.append("[" + ",".join(objects) + "]")

                writer.writerow(csv_row)

        return self.output_path
