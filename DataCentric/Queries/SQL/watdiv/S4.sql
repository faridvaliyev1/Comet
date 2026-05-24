SELECT DISTINCT T_v0."Subject" AS "v0", T_v0."http___xmlns_com_foaf_familyName" AS "v2", T_v3."Subject" AS "v3"
FROM (SELECT tables_52."Subject" AS "Subject", tables_52."http___xmlns_com_foaf_age" AS "http___xmlns_com_foaf_age", tables_52."http___xmlns_com_foaf_familyName" AS "http___xmlns_com_foaf_familyName", tables_52."http___schema_org_nationality" AS "http___schema_org_nationality"
FROM tables_52) AS T_v0
CROSS JOIN (SELECT tables_24."Subject" AS "Subject", tables_24."http___purl_org_ontology_mo_artist" AS "http___purl_org_ontology_mo_artist"
FROM tables_24) AS T_v3
WHERE T_v0."http___xmlns_com_foaf_age" = 'http://db.uwaterloo.ca/~galuc/wsdbm/AgeGroup3'
AND T_v0."http___schema_org_nationality" = 'http://db.uwaterloo.ca/~galuc/wsdbm/Country1'
AND T_v0."Subject" = T_v3."http___purl_org_ontology_mo_artist"
