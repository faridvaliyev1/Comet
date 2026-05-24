SELECT DISTINCT T_v0."Subject" AS "v0", T_v0."http___schema_org_jobTitle" AS "v1", T_const_1."http___www_geonames_org_ontology_parentCountry" AS "v3"
FROM (SELECT tables_52."Subject" AS "Subject", tables_52."http___schema_org_jobTitle" AS "http___schema_org_jobTitle", tables_52."http___schema_org_nationality" AS "http___schema_org_nationality"
FROM tables_52) AS T_v0
CROSS JOIN (SELECT tables_20."Subject" AS "Subject", tables_20."http___www_geonames_org_ontology_parentCountry" AS "http___www_geonames_org_ontology_parentCountry"
FROM tables_20) AS T_const_1
WHERE T_const_1."Subject" = 'http://db.uwaterloo.ca/~galuc/wsdbm/City72'
AND T_const_1."http___www_geonames_org_ontology_parentCountry" = T_v0."http___schema_org_nationality"
