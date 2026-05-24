SELECT DISTINCT T_v0."Subject" AS "v0", T_v0."http___purl_org_dc_terms_Location" AS "v1", T_v0."http___db_uwaterloo_ca__galuc_wsdbm_gender" AS "v3"
FROM (SELECT tables_52."Subject" AS "Subject", tables_52."http___purl_org_dc_terms_Location" AS "http___purl_org_dc_terms_Location", tables_52."http___schema_org_nationality" AS "http___schema_org_nationality", tables_52."http___db_uwaterloo_ca__galuc_wsdbm_gender" AS "http___db_uwaterloo_ca__galuc_wsdbm_gender", tables_0."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type"
FROM tables_52
FULL JOIN tables_0 ON tables_0."Subject" = tables_52."Subject") AS T_v0
WHERE T_v0."http___schema_org_nationality" = 'http://db.uwaterloo.ca/~galuc/wsdbm/Country8'
AND T_v0."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" = 'http://db.uwaterloo.ca/~galuc/wsdbm/Role2'
