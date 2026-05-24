SELECT DISTINCT T_doc."http___purl_org_dc_elements_1_1_title" AS "title"
FROM (SELECT tables_0."Subject" AS "Subject", tables_0."http___www_w3_org_2000_01_rdf_schema_subClassOf" AS "http___www_w3_org_2000_01_rdf_schema_subClassOf"
FROM tables_0) AS T_class
CROSS JOIN (SELECT tables_14."Subject" AS "Subject", tables_14."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_14."http___purl_org_dc_elements_1_1_title" AS "http___purl_org_dc_elements_1_1_title"
FROM tables_14) AS T_doc
CROSS JOIN (SELECT tables_20."Subject" AS "Subject", tables_20."http___purl_org_dc_terms_references" AS "http___purl_org_dc_terms_references"
FROM tables_20) AS T_doc2
CROSS JOIN (SELECT tables_0."Subject" AS "Subject", tables_0."http___www_w3_org_2000_01_rdf_schema_subClassOf" AS "http___www_w3_org_2000_01_rdf_schema_subClassOf"
FROM tables_0) AS T_class3
CROSS JOIN (SELECT tables_14."Subject" AS "Subject", tables_14."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_20."http___purl_org_dc_terms_references" AS "http___purl_org_dc_terms_references"
FROM tables_14
FULL JOIN tables_20 ON tables_20."Subject" = tables_14."Subject") AS T_doc3
CROSS JOIN (SELECT tables_0."Subject" AS "Subject", tables_0."http___www_w3_org_2000_01_rdf_schema_subClassOf" AS "http___www_w3_org_2000_01_rdf_schema_subClassOf"
FROM tables_0) AS T_class4
CROSS JOIN (SELECT tables_14."Subject" AS "Subject", tables_14."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_20."http___purl_org_dc_terms_references" AS "http___purl_org_dc_terms_references"
FROM tables_14
FULL JOIN tables_20 ON tables_20."Subject" = tables_14."Subject") AS T_doc4
WHERE T_class."http___www_w3_org_2000_01_rdf_schema_subClassOf" = 'http://xmlns.com/foaf/0.1/Document'
AND T_class3."http___www_w3_org_2000_01_rdf_schema_subClassOf" = 'http://xmlns.com/foaf/0.1/Document'
AND T_class4."http___www_w3_org_2000_01_rdf_schema_subClassOf" = 'http://xmlns.com/foaf/0.1/Document'
AND T_class."Subject" = T_doc."http___www_w3_org_1999_02_22_rdf_syntax_ns_type"
AND T_class3."Subject" = T_doc3."http___www_w3_org_1999_02_22_rdf_syntax_ns_type"
AND T_class4."Subject" = T_doc4."http___www_w3_org_1999_02_22_rdf_syntax_ns_type"
