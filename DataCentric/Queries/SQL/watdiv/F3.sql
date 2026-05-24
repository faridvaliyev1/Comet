SELECT DISTINCT T_v0."Subject" AS "v0", T_v0."http___schema_org_contentRating" AS "v1", T_v0."http___schema_org_contentSize" AS "v2", T_v4."Subject" AS "v4", T_v4."http___db_uwaterloo_ca__galuc_wsdbm_makesPurchase" AS "v5", T_v5."http___db_uwaterloo_ca__galuc_wsdbm_purchaseDate" AS "v6"
FROM (SELECT tables_52."Subject" AS "Subject", tables_52."http___schema_org_contentRating" AS "http___schema_org_contentRating", tables_52."http___schema_org_contentSize" AS "http___schema_org_contentSize", tables_52."http___db_uwaterloo_ca__galuc_wsdbm_hasGenre" AS "http___db_uwaterloo_ca__galuc_wsdbm_hasGenre"
FROM tables_52) AS T_v0
CROSS JOIN (SELECT tables_3."Subject" AS "Subject", tables_3."http___db_uwaterloo_ca__galuc_wsdbm_makesPurchase" AS "http___db_uwaterloo_ca__galuc_wsdbm_makesPurchase"
FROM tables_3) AS T_v4
CROSS JOIN (SELECT tables_50."Subject" AS "Subject", tables_50."http___db_uwaterloo_ca__galuc_wsdbm_purchaseDate" AS "http___db_uwaterloo_ca__galuc_wsdbm_purchaseDate", tables_50."http___db_uwaterloo_ca__galuc_wsdbm_purchaseFor" AS "http___db_uwaterloo_ca__galuc_wsdbm_purchaseFor"
FROM tables_50) AS T_v5
WHERE T_v0."http___db_uwaterloo_ca__galuc_wsdbm_hasGenre" = 'http://db.uwaterloo.ca/~galuc/wsdbm/SubGenre64'
AND T_v0."Subject" = T_v5."http___db_uwaterloo_ca__galuc_wsdbm_purchaseFor"
AND T_v4."http___db_uwaterloo_ca__galuc_wsdbm_makesPurchase" = T_v5."Subject"
AND T_v4."http___db_uwaterloo_ca__galuc_wsdbm_makesPurchase" = T_v5."Subject"
