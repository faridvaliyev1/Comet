SELECT DISTINCT *
FROM (SELECT tables_14."Subject" AS "Subject", tables_14."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type"
FROM tables_14) AS T_const_0
WHERE T_const_0."Subject" = 'http://localhost/persons/John_Q_Public'
AND T_const_0."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" = 'http://xmlns.com/foaf/0.1/Person'
