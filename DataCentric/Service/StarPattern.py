from Service.RDFWidePropertyTable import RDFWidePropertyTable
from Service.SparqlWorkload import SparqlWorkload


class StarPattern:
    def __init__(self, workload):
        self.workload = workload
        self.sparql_workload = SparqlWorkload(workload)
        self.prefix = {}
        self.stars, self.connectors = self.find_stars()

    def find_stars(self):
        stars = {}
        star_connectors = []

        for query_counter, (_path, query) in enumerate(self.sparql_workload.read_queries(), start=1):
            star_properties = {}
            objects = []

            for subject, predicate, obj in self.sparql_workload.triple_patterns(query):
                if predicate.startswith("?"):
                    continue

                property_name = RDFWidePropertyTable.normalize_uri(predicate)

                if property_name == "http___www_w3_org_1999_02_22_rdf_syntax_ns_type":
                    continue

                star_properties.setdefault(subject, []).append(property_name)

                if obj.startswith("?") or obj.startswith("http://") or obj.startswith("https://"):
                    objects.append((obj, property_name))

            stars["query" + str(query_counter)] = star_properties

            for obj, property_name in objects:
                if obj in star_properties:
                    star_connectors.append(property_name)

        return stars, set(star_connectors)

    def combine_stars(self):
        stars_dict = {}
        counter = 0

        for _key, value in self.stars.items():
            for _subject, properties in value.items():
                is_combined = False

                if len(stars_dict) == 0:
                    stars_dict["star" + str(counter)] = properties
                    counter += 1
                    is_combined = True
                else:
                    for star_key, star_properties in stars_dict.items():
                        if len(list(set(properties).intersection(set(star_properties)))) != 0:
                            stars_dict[star_key] = list(set(properties).union(set(star_properties)))
                            is_combined = True

                if is_combined == False:
                    counter += 1
                    stars_dict["star" + str(counter)] = properties

        for key, properties in stars_dict.items():
            for other_key, other_properties in stars_dict.items():
                if key != other_key and len(list(set(properties).intersection(other_properties))) != 0:
                    union = list(set(properties).union(other_properties))
                    stars_dict[other_key] = union
                    stars_dict[key] = ()

        return stars_dict

    def find_prefix(self):
        return {}
