SELECT DISTINCT T_v0."Subject" AS "v0", T_v0."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "v1", T_v0."http___schema_org_text" AS "v2"
FROM (SELECT tables_0."Subject" AS "Subject", tables_0."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_26."http___schema_org_text" AS "http___schema_org_text"
FROM tables_0
FULL JOIN tables_26 ON tables_26."Subject" = tables_0."Subject") AS T_v0
CROSS JOIN (SELECT tables_1."Subject" AS "Subject", tables_1."http___db_uwaterloo_ca__galuc_wsdbm_likes" AS "http___db_uwaterloo_ca__galuc_wsdbm_likes"
FROM tables_1) AS T_const_2
WHERE T_const_2."Subject" = 'http://db.uwaterloo.ca/~galuc/wsdbm/User659'
AND T_v0."Subject" = T_const_2."http___db_uwaterloo_ca__galuc_wsdbm_likes"
