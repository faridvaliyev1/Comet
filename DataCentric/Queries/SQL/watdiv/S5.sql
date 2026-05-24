SELECT DISTINCT T_v0."Subject" AS "v0", T_v0."http___schema_org_description" AS "v2", T_v0."http___schema_org_keywords" AS "v3"
FROM (SELECT tables_52."Subject" AS "Subject", tables_0."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_52."http___schema_org_description" AS "http___schema_org_description", tables_52."http___schema_org_keywords" AS "http___schema_org_keywords", tables_52."http___schema_org_language" AS "http___schema_org_language"
FROM tables_52
FULL JOIN tables_0 ON tables_0."Subject" = tables_52."Subject") AS T_v0
WHERE T_v0."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" = 'http://db.uwaterloo.ca/~galuc/wsdbm/ProductCategory5'
AND T_v0."http___schema_org_language" = 'http://db.uwaterloo.ca/~galuc/wsdbm/Language0'
