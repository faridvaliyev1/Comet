SELECT DISTINCT T_v0."Subject" AS "v0", T_v0."http___db_uwaterloo_ca__galuc_wsdbm_likes" AS "v1"
FROM (SELECT tables_1."Subject" AS "Subject", tables_1."http___db_uwaterloo_ca__galuc_wsdbm_likes" AS "http___db_uwaterloo_ca__galuc_wsdbm_likes", tables_1."http___db_uwaterloo_ca__galuc_wsdbm_subscribes" AS "http___db_uwaterloo_ca__galuc_wsdbm_subscribes"
FROM tables_1) AS T_v0
WHERE T_v0."http___db_uwaterloo_ca__galuc_wsdbm_subscribes" = 'http://db.uwaterloo.ca/~galuc/wsdbm/Website22'
