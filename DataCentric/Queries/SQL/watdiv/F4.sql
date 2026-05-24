SELECT DISTINCT T_v0."Subject" AS "v0", T_v0."http___xmlns_com_foaf_homepage" AS "v1", T_v2."Subject" AS "v2", T_v0."http___schema_org_description" AS "v4", T_v1."http___schema_org_url" AS "v5", T_v1."http___db_uwaterloo_ca__galuc_wsdbm_hits" AS "v6", T_v7."Subject" AS "v7", T_v0."http___schema_org_contentSize" AS "v8"
FROM (SELECT tables_52."Subject" AS "Subject", tables_52."http___xmlns_com_foaf_homepage" AS "http___xmlns_com_foaf_homepage", tables_52."http___ogp_me_ns_tag" AS "http___ogp_me_ns_tag", tables_52."http___schema_org_description" AS "http___schema_org_description", tables_52."http___schema_org_contentSize" AS "http___schema_org_contentSize"
FROM tables_52) AS T_v0
CROSS JOIN (SELECT tables_14."Subject" AS "Subject", tables_14."http___purl_org_goodrelations_includes" AS "http___purl_org_goodrelations_includes"
FROM tables_14) AS T_v2
CROSS JOIN (SELECT tables_52."Subject" AS "Subject", tables_52."http___schema_org_url" AS "http___schema_org_url", tables_52."http___db_uwaterloo_ca__galuc_wsdbm_hits" AS "http___db_uwaterloo_ca__galuc_wsdbm_hits", tables_52."http___schema_org_language" AS "http___schema_org_language"
FROM tables_52) AS T_v1
CROSS JOIN (SELECT tables_1."Subject" AS "Subject", tables_1."http___db_uwaterloo_ca__galuc_wsdbm_likes" AS "http___db_uwaterloo_ca__galuc_wsdbm_likes"
FROM tables_1) AS T_v7
WHERE T_v0."http___ogp_me_ns_tag" = 'http://db.uwaterloo.ca/~galuc/wsdbm/Topic111'
AND T_v1."http___schema_org_language" = 'http://db.uwaterloo.ca/~galuc/wsdbm/Language0'
AND T_v0."Subject" = T_v2."http___purl_org_goodrelations_includes"
AND T_v0."Subject" = T_v7."http___db_uwaterloo_ca__galuc_wsdbm_likes"
AND T_v0."http___xmlns_com_foaf_homepage" = T_v1."Subject"
AND T_v0."http___xmlns_com_foaf_homepage" = T_v1."Subject"
AND T_v0."http___xmlns_com_foaf_homepage" = T_v1."Subject"
