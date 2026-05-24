SELECT DISTINCT T_v0."Subject" AS "v0", T_v2."Subject" AS "v2", T_v2."http___schema_org_caption" AS "v3"
FROM (SELECT tables_1."Subject" AS "Subject", tables_1."http___db_uwaterloo_ca__galuc_wsdbm_subscribes" AS "http___db_uwaterloo_ca__galuc_wsdbm_subscribes", tables_1."http___db_uwaterloo_ca__galuc_wsdbm_likes" AS "http___db_uwaterloo_ca__galuc_wsdbm_likes"
FROM tables_1) AS T_v0
CROSS JOIN (SELECT tables_28."Subject" AS "Subject", tables_28."http___schema_org_caption" AS "http___schema_org_caption"
FROM tables_28) AS T_v2
WHERE T_v0."http___db_uwaterloo_ca__galuc_wsdbm_subscribes" = 'http://db.uwaterloo.ca/~galuc/wsdbm/Website22'
AND T_v2."Subject" = T_v0."http___db_uwaterloo_ca__galuc_wsdbm_likes"
