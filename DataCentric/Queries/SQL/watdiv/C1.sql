SELECT DISTINCT T_v0."Subject" AS "v0", T_v0."http___purl_org_stuff_rev_hasReview" AS "v4", T_v4."http___purl_org_stuff_rev_reviewer" AS "v6", T_v7."Subject" AS "v7"
FROM (SELECT tables_52."Subject" AS "Subject", tables_52."http___schema_org_caption" AS "http___schema_org_caption", tables_52."http___schema_org_text" AS "http___schema_org_text", tables_52."http___schema_org_contentRating" AS "http___schema_org_contentRating", tables_52."http___purl_org_stuff_rev_hasReview" AS "http___purl_org_stuff_rev_hasReview"
FROM tables_52) AS T_v0
CROSS JOIN (SELECT tables_47."Subject" AS "Subject", tables_47."http___purl_org_stuff_rev_title" AS "http___purl_org_stuff_rev_title", tables_47."http___purl_org_stuff_rev_reviewer" AS "http___purl_org_stuff_rev_reviewer"
FROM tables_47) AS T_v4
CROSS JOIN (SELECT tables_52."Subject" AS "Subject", tables_52."http___schema_org_actor" AS "http___schema_org_actor", tables_52."http___schema_org_language" AS "http___schema_org_language"
FROM tables_52) AS T_v7
WHERE T_v0."http___purl_org_stuff_rev_hasReview" = T_v4."Subject"
AND T_v0."http___purl_org_stuff_rev_hasReview" = T_v4."Subject"
AND T_v4."http___purl_org_stuff_rev_reviewer" = T_v7."http___schema_org_actor"
