SELECT DISTINCT T_author1."http___xmlns_com_foaf_0_1_name" AS "name1", T_author2."http___xmlns_com_foaf_0_1_name" AS "name2"
FROM (SELECT tables_15."Subject" AS "Subject", tables_14."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_15."http___purl_org_dc_elements_1_1_creator" AS "http___purl_org_dc_elements_1_1_creator", tables_15."http___swrc_ontoware_org_ontology_journal" AS "http___swrc_ontoware_org_ontology_journal"
FROM tables_15
FULL JOIN tables_14 ON tables_14."Subject" = tables_15."Subject") AS T_article1
CROSS JOIN (SELECT tables_15."Subject" AS "Subject", tables_14."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_15."http___purl_org_dc_elements_1_1_creator" AS "http___purl_org_dc_elements_1_1_creator", tables_15."http___swrc_ontoware_org_ontology_journal" AS "http___swrc_ontoware_org_ontology_journal"
FROM tables_15
FULL JOIN tables_14 ON tables_14."Subject" = tables_15."Subject") AS T_article2
CROSS JOIN (SELECT tables_1."Subject" AS "Subject", tables_1."http___xmlns_com_foaf_0_1_name" AS "http___xmlns_com_foaf_0_1_name"
FROM tables_1) AS T_author1
CROSS JOIN (SELECT tables_1."Subject" AS "Subject", tables_1."http___xmlns_com_foaf_0_1_name" AS "http___xmlns_com_foaf_0_1_name"
FROM tables_1) AS T_author2
WHERE T_article1."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" = 'http://localhost/vocabulary/bench/Article'
AND T_article2."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" = 'http://localhost/vocabulary/bench/Article'
AND T_article1."http___purl_org_dc_elements_1_1_creator" = T_author1."Subject"
AND T_article2."http___purl_org_dc_elements_1_1_creator" = T_author2."Subject"
AND T_article1."http___swrc_ontoware_org_ontology_journal" = T_article2."http___swrc_ontoware_org_ontology_journal"
