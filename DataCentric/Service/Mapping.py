from Utils.DBContext import DbContext, conn
import os

class Mapping:
    def __init__(self, Tables):
        self.Tables = Tables
        self.initialize()

    # ---------- private functions ----------

    def initialize(self):
        DbContext.Insert("DROP TABLE IF EXISTS GLOBAL_MAPPING", None)

        for index in range(len(self.Tables)):
            table_cluster = self.Tables[index]

            if table_cluster is None:
                print(f"Skipping tables_{index}: cluster is None")
                continue

            if len(table_cluster) == 0:
                print(f"Skipping tables_{index}: empty cluster")
                continue

            self.createMapping(table_cluster, "tables_" + str(index))

    def partition_wpt(self, Cluster):
        pass

    def DropColumn(self, Columns, table_name):
        for column in Columns.split(','):
            column = column.strip()

            if column == "":
                continue

            sql = f"""
            ALTER TABLE {table_name} DROP COLUMN {column};
            """

            DbContext.Insert(sql, None)

    def find_columns_information(self, Cluster):
        if Cluster is None or len(Cluster) == 0:
            return []

        quoted_columns = []

        for item in Cluster:
            if item is None:
                continue

            item = str(item).strip()

            if item == "":
                continue

            # Escape single quotes for SQL string literals
            item = item.replace("'", "''")
            quoted_columns.append("'" + item + "'")

        if len(quoted_columns) == 0:
            return []

        columns = ",".join(quoted_columns)

        sql = f"""
        SELECT COLUMN_NAME, TYPE_NAME
        FROM METRICS
        WHERE COLUMN_NAME IN ({columns})
        """

        data = DbContext.Select(sql)

        if data is None:
            return []

        return data

    def Create_Table(self, Table, Columns):
        if Columns is None or len(Columns) == 0:
            print(f"Skipping table creation for {Table}: no columns found")
            return False

        column_definitions = []

        for element in Columns:
            if element is None or len(element) < 2:
                continue

            column_name = str(element[0]).strip()
            column_type = str(element[1]).strip()

            if column_name == "" or column_type == "":
                continue

            # Quote column names because your property names contain underscores/special forms
            column_definitions.append(f'"{column_name}" {column_type}')

        if len(column_definitions) == 0:
            print(f"Skipping table creation for {Table}: no valid column definitions")
            return False

        columns_sql = ",\n        ".join(column_definitions)

        sql = f"""
        DROP TABLE IF EXISTS {Table};

        CREATE TABLE {Table}(
            "Subject" VarChar,
            {columns_sql}
        );
        """

        print(f"Creating table: {Table}")
        DbContext.Insert(sql, None)

        return True

    def fill_data(self, Table, Columns):
        if Columns is None or Columns.strip() == "":
            print(f"Skipping fill_data for {Table}: no columns")
            return

        sql = f"""
        INSERT INTO {Table}
        SELECT DISTINCT "Subject", {Columns}
        FROM wpt_tbl
        WHERE
        """

        conditions = []

        for column in Columns.split(','):
            column = column.strip()

            if column == "":
                continue

            conditions.append(f"{column} IS NOT NULL")

        if len(conditions) == 0:
            print(f"Skipping fill_data for {Table}: no valid WHERE conditions")
            return

        sql += " OR ".join(conditions)

        DbContext.Insert(sql, None)

    def create_global_mapping(self, Table, Columns):
        if Columns is None or len(Columns) == 0:
            print(f"Skipping global mapping for {Table}: no columns")
            return

        sql = """
        CREATE TABLE IF NOT EXISTS GLOBAL_MAPPING(
            COLUMN_NAME text,
            TABLE_NAME text
        );
        """

        DbContext.Insert(sql, None)

        for column in Columns:
            if column is None or len(column) == 0:
                continue

            DbContext.Insert(
                "INSERT INTO GLOBAL_MAPPING (COLUMN_NAME, TABLE_NAME) VALUES (%s, %s)",
                [(column[0], Table)]
            )

    def createMapping(self, Cluster, Table_Name):
        columns = self.find_columns_information(Cluster)

        if columns is None or len(columns) == 0:
            print("-------------------------------------")
            print(f"Skipping {Table_Name}: no matching columns found in METRICS")
            print("Cluster was:")
            print(Cluster)
            print("-------------------------------------")
            return

        table_created = self.Create_Table(Table_Name, columns)

        if not table_created:
            return

        cols_list = []

        for column in columns:
            if column is None or len(column) == 0:
                continue

            column_name = str(column[0]).strip()

            if column_name == "":
                continue

            cols_list.append(f'"{column_name}"')

        if len(cols_list) == 0:
            print(f"Skipping {Table_Name}: no valid columns for insert")
            return

        cols = ",".join(cols_list)

        self.fill_data(Table_Name, cols)
        self.create_global_mapping(Table_Name, columns)

        # self.DropColumn(cols, "wpt_tbl")

        sql = """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'wpt_tbl'
        AND table_schema = 'public'
        """

        columns = DbContext.Select(sql)

    # ---------- end of private functions ----------

    def copy_to_table(self, output_dir="Data/results/h2o"):
        sql = "SELECT DISTINCT TABLE_NAME FROM GLOBAL_MAPPING"

        tables = DbContext.Select(sql)

        if tables is None or len(tables) == 0:
            print("No tables found in GLOBAL_MAPPING. Nothing to export.")
            return

        os.makedirs(output_dir, exist_ok=True)
        
        for table in tables:
            table_name = table[0]

            sql = f"COPY (SELECT * FROM {table_name}) TO STDOUT WITH CSV HEADER"

            cursor = conn.cursor()

            # output_path = "Data/results2/h20_100M/" + f"{table_name}.csv"
            output_path = os.path.join(output_dir, f"{table_name}.csv")

            with open(output_path, "w") as file:
                cursor.copy_expert(sql, file)

            print(f"Exported {table_name} to {output_path}")
