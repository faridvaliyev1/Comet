import argparse
from pathlib import Path

from Utils.Helper import Helper
from Utils.DataStructures import DataStructures
from Utils.DBContext import DbContext

from Service.Clustering import Clustering
from Service.Mapping import Mapping
from Service.Partitioning import Partitioning
from Service.RDFWidePropertyTable import RDFWidePropertyTable
from Service.StarPattern import StarPattern
from Configurations import NULL_THRESHOLD
from query_converter import convert_workload


def parse_args():
    parser = argparse.ArgumentParser(description="Generate a data-centric schema from an RDF dataset and SPARQL workload.")
    parser.add_argument(
        "--dataset",
        default="Data/watdiv/watdiv.nt",
        help="Input RDF dataset file or directory. Supported files: .nt, .n3, .ttl, .rdf",
    )
    parser.add_argument(
        "--rdf-format",
        choices=["nt", "n3"],
        default=None,
        help="RDF format override. Defaults to the dataset file extension.",
    )
    parser.add_argument(
        "--workload",
        default="Queries/SPARQL/watdiv",
        help="SPARQL workload file or directory.",
    )
    parser.add_argument(
        "--wpt-output",
        default=None,
        help="Optional output CSV path for the generated wide property table.",
    )
    parser.add_argument(
        "--converted-output",
        default=None,
        help="Output directory for SQL converted from the SPARQL workload. Defaults to Queries/SQL/<dataset-name>.",
    )
    parser.add_argument(
        "--dataset-name",
        default=None,
        help="Dataset name used for converted SQL output folder. Defaults to the workload folder name.",
    )
    parser.add_argument(
        "--support-threshold",
        type=float,
        default=0.5,
        help="Support threshold used by the existing clustering logic.",
    )
    parser.add_argument(
        "--null-threshold",
        type=int,
        default=15,
        help="Null threshold used by the existing partitioning logic.",
    )

    return parser.parse_args()


def generate_wpt(dataset, output_path, rdf_format):
    print("---RDF dataset is converting to WPT CSV------")

    generator = RDFWidePropertyTable(
        dataset_path=dataset,
        output_path=output_path,
        rdf_format=rdf_format,
    )
    wpt_path = generator.generate()

    print(f"---WPT CSV generated: {wpt_path}------")
    return wpt_path


def run_pipeline(args):
    print("---Application is starting------")

    wpt_path = generate_wpt(args.dataset, args.wpt_output, args.rdf_format)

    print("---CSV is importing--------")
    DbContext.Save_Csv_To_Sql(str(wpt_path))
    print("---End of importing------")

    print("----Metrics calculation------------")
    columns = Helper.GetColumnInformation()
    Helper.CalculateMetrics(columns)
    print("----End of metrics calculation------------")

    print("Data Structure generation")
    print("end of data structure generation")

    print("Clustering starting...")

    support_thresholds = [args.support_threshold]
    null_thresholds = [args.null_threshold]
    property_usage_list = []
    partitioning = None

    for support_threshold in support_thresholds:
        data_structures = DataStructures(support_threshold)

        for null_threshold in null_thresholds:
            clustering = Clustering(
                data_structures.SubjectPropertyBasket,
                data_structures.Subject_PropertyBasketCount,
                data_structures.PropertyUsageList,
                data_structures.Fpgrowth_list,
                support_threshold,
                null_threshold,
            )

            partitioning = Partitioning(
                clustering.Clusters,
                clustering.Tables,
                data_structures.PropertyUsageList,
                null_threshold,
            )

            tables_count = 0
            for part in partitioning.Tables:
                if part is not None:
                    tables_count += 1

            property_usage_list = data_structures.PropertyUsageList

            print("-----------------------------------")
            print(
                f"Support_Threshold: {support_threshold} \n"
                f" Null_Threshold: {null_threshold} \n"
                f" Number of tables: {tables_count} "
            )
            print("------------------------------------")

    star_pattern = StarPattern(args.workload)

    connectors = star_pattern.find_stars()[1]
    star_tables = star_pattern.combine_stars()

    stars = []
    for _key, value in star_tables.items():
        if len(value) > 0:
            stars.append(tuple(value))

    for index in range(len(stars)):
        print(index, ":", stars[index])
        print("--------------------")

    for tables in partitioning.Tables:
        if len(tables) != 1:
            for table in tables:
                for star in stars:
                    if table in star and (property_usage_list[table] / property_usage_list["Subject"]) > NULL_THRESHOLD:
                        tuple(t for t in tables if t != table)

    for tables in partitioning.Tables:
        if len(tables) != 1:
            for table in tables:
                for connector in connectors:
                    if connector in table and (property_usage_list[table] / property_usage_list["Subject"]) > NULL_THRESHOLD:
                        tuple(t for t in tables if t != table)
            print("-------------------------------------")

    for star in stars:
        partitioning.Tables.append(star)

    mapping = Mapping(partitioning.Tables)
    mapping.copy_to_table()

    print("---SPARQL workload is converting to SQL--------")
    converted_count, converted_output = convert_workload(
        args.workload,
        args.converted_output,
        args.dataset_name,
    )
    print(f"Converted {converted_count} workload query/query block(s) to {converted_output}")


if __name__ == "__main__":
    run_pipeline(parse_args())
