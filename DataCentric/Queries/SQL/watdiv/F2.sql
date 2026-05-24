SELECT DISTINCT T_v0."Subject" AS "v0", T_v0."http___xmlns_com_foaf_homepage" AS "v1", T_v0."http___ogp_me_ns_title" AS "v2", T_v0."http___schema_org_caption" AS "v4", T_v0."http___schema_org_description" AS "v5", T_v1."http___schema_org_url" AS "v6", T_v1."http___db_uwaterloo_ca__galuc_wsdbm_hits" AS "v7"
FROM (SELECT tables_52."Subject" AS "Subject", tables_52."http___xmlns_com_foaf_homepage" AS "http___xmlns_com_foaf_homepage", tables_52."http___ogp_me_ns_title" AS "http___ogp_me_ns_title", tables_0."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_52."http___schema_org_caption" AS "http___schema_org_caption", tables_52."http___schema_org_description" AS "http___schema_org_description", tables_52."http___db_uwaterloo_ca__galuc_wsdbm_hasGenre" AS "http___db_uwaterloo_ca__galuc_wsdbm_hasGenre"
FROM tables_52
FULL JOIN tables_0 ON tables_0."Subject" = tables_52."Subject") AS T_v0
CROSS JOIN (SELECT tables_10."Subject" AS "Subject", tables_10."http___schema_org_url" AS "http___schema_org_url", tables_10."http___db_uwaterloo_ca__galuc_wsdbm_hits" AS "http___db_uwaterloo_ca__galuc_wsdbm_hits"
FROM tables_10) AS T_v1
WHERE T_v0."http___db_uwaterloo_ca__galuc_wsdbm_hasGenre" = 'http://db.uwaterloo.ca/~galuc/wsdbm/SubGenre64'
AND T_v0."http___xmlns_com_foaf_homepage" = T_v1."Subject"
AND T_v0."http___xmlns_com_foaf_homepage" = T_v1."Subject"
