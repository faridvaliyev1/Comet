SELECT DISTINCT T_v0."Subject" AS "v0", T_v2."http___purl_org_goodrelations_includes" AS "v3", T_v4."Subject" AS "v4", T_v3."http___purl_org_stuff_rev_hasReview" AS "v8"
FROM (SELECT tables_48."Subject" AS "Subject", tables_48."http___schema_org_legalName" AS "http___schema_org_legalName", tables_48."http___purl_org_goodrelations_offers" AS "http___purl_org_goodrelations_offers"
FROM tables_48) AS T_v0
CROSS JOIN (SELECT tables_14."Subject" AS "Subject", tables_14."http___schema_org_eligibleRegion" AS "http___schema_org_eligibleRegion", tables_14."http___purl_org_goodrelations_includes" AS "http___purl_org_goodrelations_includes"
FROM tables_14) AS T_v2
CROSS JOIN (SELECT tables_52."Subject" AS "Subject", tables_52."http___schema_org_jobTitle" AS "http___schema_org_jobTitle", tables_52."http___xmlns_com_foaf_homepage" AS "http___xmlns_com_foaf_homepage", tables_52."http___db_uwaterloo_ca__galuc_wsdbm_makesPurchase" AS "http___db_uwaterloo_ca__galuc_wsdbm_makesPurchase"
FROM tables_52) AS T_v4
CROSS JOIN (SELECT tables_11."Subject" AS "Subject", tables_11."http___db_uwaterloo_ca__galuc_wsdbm_purchaseFor" AS "http___db_uwaterloo_ca__galuc_wsdbm_purchaseFor"
FROM tables_11) AS T_v7
CROSS JOIN (SELECT tables_29."Subject" AS "Subject", tables_29."http___purl_org_stuff_rev_hasReview" AS "http___purl_org_stuff_rev_hasReview"
FROM tables_29) AS T_v3
CROSS JOIN (SELECT tables_12."Subject" AS "Subject", tables_12."http___purl_org_stuff_rev_totalVotes" AS "http___purl_org_stuff_rev_totalVotes"
FROM tables_12) AS T_v8
WHERE T_v2."http___schema_org_eligibleRegion" = 'http://db.uwaterloo.ca/~galuc/wsdbm/Country5'
AND T_v0."http___purl_org_goodrelations_offers" = T_v2."Subject"
AND T_v0."http___purl_org_goodrelations_offers" = T_v2."Subject"
AND T_v2."http___purl_org_goodrelations_includes" = T_v7."http___db_uwaterloo_ca__galuc_wsdbm_purchaseFor"
AND T_v2."http___purl_org_goodrelations_includes" = T_v3."Subject"
AND T_v4."http___db_uwaterloo_ca__galuc_wsdbm_makesPurchase" = T_v7."Subject"
AND T_v3."http___purl_org_stuff_rev_hasReview" = T_v8."Subject"
