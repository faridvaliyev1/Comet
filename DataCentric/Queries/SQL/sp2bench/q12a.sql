SELECT DISTINCT *
FROM (SELECT tables_12."Subject" AS "Subject", tables_14."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_12."http___purl_org_dc_elements_1_1_creator" AS "http___purl_org_dc_elements_1_1_creator"
FROM tables_12
FULL JOIN tables_14 ON tables_14."Subject" = tables_12."Subject") AS T_article
CROSS JOIN (SELECT tables_12."Subject" AS "Subject", tables_14."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_12."http___purl_org_dc_elements_1_1_creator" AS "http___purl_org_dc_elements_1_1_creator"
FROM tables_12
FULL JOIN tables_14 ON tables_14."Subject" = tables_12."Subject") AS T_inproc
CROSS JOIN (SELECT tables_1."Subject" AS "Subject", tables_1."http___xmlns_com_foaf_0_1_name" AS "http___xmlns_com_foaf_0_1_name"
FROM tables_1) AS T_person1
CROSS JOIN (SELECT tables_1."Subject" AS "Subject", tables_1."http___xmlns_com_foaf_0_1_name" AS "http___xmlns_com_foaf_0_1_name"
FROM tables_1) AS T_person2
WHERE T_article."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" = 'http://localhost/vocabulary/bench/Article'
AND T_inproc."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" = 'http://localhost/vocabulary/bench/Inproceedings'
AND T_article."http___purl_org_dc_elements_1_1_creator" = T_person1."Subject"
AND T_inproc."http___purl_org_dc_elements_1_1_creator" = T_person2."Subject"
