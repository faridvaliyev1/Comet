SELECT DISTINCT T_v0."Subject" AS "v0", T_v0."http___purl_org_goodrelations_includes" AS "v1", T_v0."http___purl_org_goodrelations_price" AS "v3", T_v0."http___purl_org_goodrelations_validThrough" AS "v4", T_v1."http___ogp_me_ns_title" AS "v5", T_v1."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "v6"
FROM (SELECT tables_49."Subject" AS "Subject", tables_49."http___purl_org_goodrelations_includes" AS "http___purl_org_goodrelations_includes", tables_49."http___purl_org_goodrelations_price" AS "http___purl_org_goodrelations_price", tables_49."http___purl_org_goodrelations_validThrough" AS "http___purl_org_goodrelations_validThrough"
FROM tables_49) AS T_v0
CROSS JOIN (SELECT tables_17."Subject" AS "Subject", tables_17."http___purl_org_goodrelations_offers" AS "http___purl_org_goodrelations_offers"
FROM tables_17) AS T_const_1
CROSS JOIN (SELECT tables_0."Subject" AS "Subject", tables_23."http___ogp_me_ns_title" AS "http___ogp_me_ns_title", tables_0."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type"
FROM tables_0
FULL JOIN tables_23 ON tables_23."Subject" = tables_0."Subject") AS T_v1
WHERE T_const_1."Subject" = 'http://db.uwaterloo.ca/~galuc/wsdbm/Retailer5'
AND T_v0."Subject" = T_const_1."http___purl_org_goodrelations_offers"
AND T_v0."http___purl_org_goodrelations_includes" = T_v1."Subject"
AND T_v0."http___purl_org_goodrelations_includes" = T_v1."Subject"
