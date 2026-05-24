SELECT DISTINCT T_article."Subject" AS "article"
FROM (SELECT tables_14."Subject" AS "Subject", tables_14."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_17."http___swrc_ontoware_org_ontology_month" AS "http___swrc_ontoware_org_ontology_month"
FROM tables_14
FULL JOIN tables_17 ON tables_17."Subject" = tables_14."Subject") AS T_article
WHERE T_article."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" = 'http://localhost/vocabulary/bench/Article'
