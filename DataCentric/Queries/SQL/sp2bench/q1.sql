SELECT DISTINCT T_journal."http___purl_org_dc_terms_issued" AS "yr"
FROM (SELECT tables_15."Subject" AS "Subject", tables_14."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" AS "http___www_w3_org_1999_02_22_rdf_syntax_ns_type", tables_15."http___purl_org_dc_elements_1_1_title" AS "http___purl_org_dc_elements_1_1_title", tables_15."http___purl_org_dc_terms_issued" AS "http___purl_org_dc_terms_issued"
FROM tables_15
FULL JOIN tables_14 ON tables_14."Subject" = tables_15."Subject") AS T_journal
WHERE T_journal."http___www_w3_org_1999_02_22_rdf_syntax_ns_type" = 'http://localhost/vocabulary/bench/Journal'
AND T_journal."http___purl_org_dc_elements_1_1_title" = 'Journal 1 (1940)'
