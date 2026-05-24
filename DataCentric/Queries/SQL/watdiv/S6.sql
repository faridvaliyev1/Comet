SELECT DISTINCT T_v0."Subject" AS "v0", T_v0."http___purl_org_ontology_mo_conductor" AS "v1", T_v0."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "v2"
FROM (SELECT tables_52."Subject" AS "Subject", tables_52."http___purl_org_ontology_mo_conductor" AS "http___purl_org_ontology_mo_conductor", tables_0."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_52."http___db_uwaterloo_ca__galuc_wsdbm_hasGenre" AS "http___db_uwaterloo_ca__galuc_wsdbm_hasGenre"
FROM tables_52
FULL JOIN tables_0 ON tables_0."Subject" = tables_52."Subject") AS T_v0
WHERE T_v0."http___db_uwaterloo_ca__galuc_wsdbm_hasGenre" = 'http://db.uwaterloo.ca/~galuc/wsdbm/SubGenre44'
