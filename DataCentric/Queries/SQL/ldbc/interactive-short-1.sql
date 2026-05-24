SELECT DISTINCT T_cityIdIri."http___www_ldbc_eu_ldbc_socialnet_1_0_vocabulary_id" AS "cityId"
FROM (SELECT tables_3."Subject" AS "Subject", tables_3."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type"
FROM tables_3) AS T_const_0
CROSS JOIN (SELECT tables_3."Subject" AS "Subject", tables_3."http___www_ldbc_eu_ldbc_socialnet_1_0_vocabulary_id" AS "http___www_ldbc_eu_ldbc_socialnet_1_0_vocabulary_id"
FROM tables_3) AS T_cityIdIri
WHERE T_const_0."Subject" = 'http://www.ldbc.eu/ldbc_socialnet/1.0/data/pers%personId%'
AND T_const_0."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" = 'http://www.ldbc.eu/ldbc_socialnet/1.0/vocabulary/Person ;'
