SELECT DISTINCT T_v0."Subject" AS "v0", T_v0."http___schema_org_caption" AS "v2"
FROM (SELECT tables_52."Subject" AS "Subject", tables_52."http___ogp_me_ns_tag" AS "http___ogp_me_ns_tag", tables_52."http___schema_org_caption" AS "http___schema_org_caption"
FROM tables_52) AS T_v0
WHERE T_v0."http___ogp_me_ns_tag" = 'http://db.uwaterloo.ca/~galuc/wsdbm/Topic75'
