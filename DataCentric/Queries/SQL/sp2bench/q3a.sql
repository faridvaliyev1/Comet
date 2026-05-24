SELECT DISTINCT T_article."Subject" AS "article"
FROM (SELECT tables_11."Subject" AS "Subject", tables_14."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_11."http___swrc_ontoware_org_ontology_pages" AS "http___swrc_ontoware_org_ontology_pages"
FROM tables_11
FULL JOIN tables_14 ON tables_14."Subject" = tables_11."Subject") AS T_article
WHERE T_article."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" = 'http://localhost/vocabulary/bench/Article'
