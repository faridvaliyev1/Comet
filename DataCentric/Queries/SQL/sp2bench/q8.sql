SELECT DISTINCT T_author2."http___xmlns_com_foaf_0_1_name" AS "name"
FROM (SELECT tables_1."Subject" AS "Subject", tables_14."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_1."http___xmlns_com_foaf_0_1_name" AS "http___xmlns_com_foaf_0_1_name"
FROM tables_1
FULL JOIN tables_14 ON tables_14."Subject" = tables_1."Subject") AS T_erdoes
CROSS JOIN (SELECT tables_12."Subject" AS "Subject", tables_12."http___purl_org_dc_elements_1_1_creator" AS "http___purl_org_dc_elements_1_1_creator"
FROM tables_12) AS T_document
CROSS JOIN (SELECT tables_12."Subject" AS "Subject", tables_12."http___purl_org_dc_elements_1_1_creator" AS "http___purl_org_dc_elements_1_1_creator"
FROM tables_12) AS T_document2
CROSS JOIN (SELECT tables_1."Subject" AS "Subject", tables_1."http___xmlns_com_foaf_0_1_name" AS "http___xmlns_com_foaf_0_1_name"
FROM tables_1) AS T_author2
CROSS JOIN (SELECT tables_1."Subject" AS "Subject", tables_1."http___xmlns_com_foaf_0_1_name" AS "http___xmlns_com_foaf_0_1_name"
FROM tables_1) AS T_author
WHERE T_erdoes."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" = 'http://xmlns.com/foaf/0.1/Person'
AND T_erdoes."http___xmlns_com_foaf_0_1_name" = 'Paul Erdoes'
AND T_erdoes."Subject" = T_document."http___purl_org_dc_elements_1_1_creator"
AND T_erdoes."Subject" = T_document."http___purl_org_dc_elements_1_1_creator"
AND T_document."http___purl_org_dc_elements_1_1_creator" = T_document2."http___purl_org_dc_elements_1_1_creator"
AND T_document."http___purl_org_dc_elements_1_1_creator" = T_author."Subject"
AND T_document2."http___purl_org_dc_elements_1_1_creator" = T_author2."Subject"
AND T_author2."http___xmlns_com_foaf_0_1_name" = T_author."http___xmlns_com_foaf_0_1_name"
