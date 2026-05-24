SELECT DISTINCT T_document."http___purl_org_dc_terms_issued" AS "yr", T_author."http___xmlns_com_foaf_0_1_name" AS "name", T_document."Subject" AS "document"
FROM (SELECT tables_0."Subject" AS "Subject", tables_0."http___www_w3_org_2000_01_rdf_schema_subClassOf" AS "http___www_w3_org_2000_01_rdf_schema_subClassOf"
FROM tables_0) AS T_class
CROSS JOIN (SELECT tables_15."Subject" AS "Subject", tables_14."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_15."http___purl_org_dc_terms_issued" AS "http___purl_org_dc_terms_issued", tables_15."http___purl_org_dc_elements_1_1_creator" AS "http___purl_org_dc_elements_1_1_creator"
FROM tables_15
FULL JOIN tables_14 ON tables_14."Subject" = tables_15."Subject") AS T_document
CROSS JOIN (SELECT tables_1."Subject" AS "Subject", tables_1."http___xmlns_com_foaf_0_1_name" AS "http___xmlns_com_foaf_0_1_name"
FROM tables_1) AS T_author
CROSS JOIN (SELECT tables_0."Subject" AS "Subject", tables_0."http___www_w3_org_2000_01_rdf_schema_subClassOf" AS "http___www_w3_org_2000_01_rdf_schema_subClassOf"
FROM tables_0) AS T_class2
CROSS JOIN (SELECT tables_15."Subject" AS "Subject", tables_14."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_15."http___purl_org_dc_terms_issued" AS "http___purl_org_dc_terms_issued", tables_15."http___purl_org_dc_elements_1_1_creator" AS "http___purl_org_dc_elements_1_1_creator"
FROM tables_15
FULL JOIN tables_14 ON tables_14."Subject" = tables_15."Subject") AS T_document2
WHERE T_class."http___www_w3_org_2000_01_rdf_schema_subClassOf" = 'http://xmlns.com/foaf/0.1/Document'
AND T_class2."http___www_w3_org_2000_01_rdf_schema_subClassOf" = 'http://xmlns.com/foaf/0.1/Document'
AND T_class."Subject" = T_document."http___www_w3_org_1999_02_22_rdf_syntax_ns_type"
AND T_document."http___purl_org_dc_elements_1_1_creator" = T_author."Subject"
AND T_class2."Subject" = T_document2."http___www_w3_org_1999_02_22_rdf_syntax_ns_type"
