-- ============================================================
--  STARTUP METRICS DASHBOARD — SQL Queries
--  Author  : Pretty
--  Dataset : users.csv, events.csv, sessions.csv
--  Tool    : SQLite / PostgreSQL / BigQuery compatible
-- ============================================================

-- ─────────────────────────────────────────────────────────────
-- 1. DAILY ACTIVE USERS (DAU)
-- ─────────────────────────────────────────────────────────────
SELECT
    event_date,
    COUNT(DISTINCT user_id) AS dau
FROM events
GROUP BY event_date
ORDER BY event_date;


-- ─────────────────────────────────────────────────────────────
-- 2. MONTHLY ACTIVE USERS (MAU)
-- ─────────────────────────────────────────────────────────────
SELECT
    strftime('%Y-%m', event_date)   AS month,   -- SQLite
    -- DATE_TRUNC('month', event_date) AS month, -- PostgreSQL
    COUNT(DISTINCT user_id)         AS mau
FROM events
GROUP BY 1
ORDER BY 1;


-- ─────────────────────────────────────────────────────────────
-- 3. STICKINESS — DAU / MAU ratio
-- ─────────────────────────────────────────────────────────────
WITH
  dau AS (
    SELECT event_date,
           strftime('%Y-%m', event_date) AS month,
           COUNT(DISTINCT user_id)       AS dau
    FROM events
    GROUP BY event_date
  ),
  mau AS (
    SELECT strftime('%Y-%m', event_date) AS month,
           COUNT(DISTINCT user_id)       AS mau
    FROM events
    GROUP BY 1
  ),
  daily_avg AS (
    SELECT month, AVG(dau) AS avg_dau
    FROM dau
    GROUP BY month
  )
SELECT
    m.month,
    m.mau,
    ROUND(d.avg_dau, 0)                       AS avg_dau,
    ROUND(d.avg_dau / m.mau * 100, 1)         AS stickiness_pct
FROM mau m
JOIN daily_avg d ON m.month = d.month
ORDER BY m.month;


-- ─────────────────────────────────────────────────────────────
-- 4. CONVERSION FUNNEL
--    signup → activation → feature_use → upgrade → paying
-- ─────────────────────────────────────────────────────────────
WITH funnel AS (
  SELECT
    COUNT(DISTINCT CASE WHEN event = 'signup'       THEN user_id END) AS signup_users,
    COUNT(DISTINCT CASE WHEN event = 'activation'   THEN user_id END) AS activation_users,
    COUNT(DISTINCT CASE WHEN event = 'feature_use'  THEN user_id END) AS feature_use_users,
    COUNT(DISTINCT CASE WHEN event = 'upgrade'      THEN user_id END) AS upgrade_users,
    COUNT(DISTINCT CASE WHEN event = 'paying'       THEN user_id END) AS paying_users
  FROM events
)
SELECT
    'Signup'       AS stage, signup_users      AS users, 100.0 AS pct_of_signup FROM funnel
UNION ALL SELECT
    'Activation',   activation_users,  ROUND(activation_users  * 100.0 / signup_users, 1) FROM funnel
UNION ALL SELECT
    'Feature Use',  feature_use_users, ROUND(feature_use_users * 100.0 / signup_users, 1) FROM funnel
UNION ALL SELECT
    'Upgrade',      upgrade_users,     ROUND(upgrade_users     * 100.0 / signup_users, 1) FROM funnel
UNION ALL SELECT
    'Paying',       paying_users,      ROUND(paying_users      * 100.0 / signup_users, 1) FROM funnel;


-- ─────────────────────────────────────────────────────────────
-- 5. DROP-OFF ANALYSIS — where users leave the funnel
-- ─────────────────────────────────────────────────────────────
WITH funnel AS (
  SELECT
    COUNT(DISTINCT CASE WHEN event='signup'      THEN user_id END) AS s,
    COUNT(DISTINCT CASE WHEN event='activation'  THEN user_id END) AS a,
    COUNT(DISTINCT CASE WHEN event='feature_use' THEN user_id END) AS f,
    COUNT(DISTINCT CASE WHEN event='upgrade'     THEN user_id END) AS u,
    COUNT(DISTINCT CASE WHEN event='paying'      THEN user_id END) AS p
  FROM events
)
SELECT 'Signup → Activation'   AS step, ROUND((s-a)*100.0/s,1) AS dropoff_pct FROM funnel
UNION ALL SELECT 'Activation → Feature Use', ROUND((a-f)*100.0/a,1) FROM funnel
UNION ALL SELECT 'Feature Use → Upgrade',    ROUND((f-u)*100.0/f,1) FROM funnel
UNION ALL SELECT 'Upgrade → Paying',         ROUND((u-p)*100.0/u,1) FROM funnel;


-- ─────────────────────────────────────────────────────────────
-- 6. RETENTION — Day 1 / Day 7 / Day 30
-- ─────────────────────────────────────────────────────────────
WITH
  signup AS (
    SELECT user_id, MIN(event_date) AS signup_date
    FROM events WHERE event = 'signup'
    GROUP BY user_id
  ),
  activity AS (
    SELECT DISTINCT user_id, event_date FROM events
  ),
  retention AS (
    SELECT
      s.user_id,
      s.signup_date,
      MAX(CASE WHEN CAST(julianday(a.event_date)-julianday(s.signup_date) AS INT) BETWEEN 1  AND 2  THEN 1 ELSE 0 END) AS day1_ret,
      MAX(CASE WHEN CAST(julianday(a.event_date)-julianday(s.signup_date) AS INT) BETWEEN 6  AND 8  THEN 1 ELSE 0 END) AS day7_ret,
      MAX(CASE WHEN CAST(julianday(a.event_date)-julianday(s.signup_date) AS INT) BETWEEN 29 AND 31 THEN 1 ELSE 0 END) AS day30_ret
    FROM signup s
    LEFT JOIN activity a ON s.user_id = a.user_id
    GROUP BY s.user_id, s.signup_date
  )
SELECT
    COUNT(*)                                AS total_users,
    ROUND(SUM(day1_ret)  * 100.0 / COUNT(*), 1) AS day1_retention_pct,
    ROUND(SUM(day7_ret)  * 100.0 / COUNT(*), 1) AS day7_retention_pct,
    ROUND(SUM(day30_ret) * 100.0 / COUNT(*), 1) AS day30_retention_pct
FROM retention;


-- ─────────────────────────────────────────────────────────────
-- 7. COHORT RETENTION TABLE (monthly cohorts)
-- ─────────────────────────────────────────────────────────────
WITH
  cohorts AS (
    SELECT user_id,
           strftime('%Y-%m', MIN(event_date)) AS cohort_month
    FROM events WHERE event = 'signup'
    GROUP BY user_id
  ),
  activity AS (
    SELECT DISTINCT user_id,
           strftime('%Y-%m', event_date) AS activity_month
    FROM events
  ),
  joined AS (
    SELECT c.user_id, c.cohort_month, a.activity_month,
           (strftime('%Y', a.activity_month)*12 + strftime('%m', a.activity_month)) -
           (strftime('%Y', c.cohort_month)*12  + strftime('%m', c.cohort_month)) AS period
    FROM cohorts c
    JOIN activity a ON c.user_id = a.user_id
  )
SELECT
    cohort_month,
    period,
    COUNT(DISTINCT user_id)                                               AS active_users,
    ROUND(COUNT(DISTINCT user_id) * 100.0 /
          FIRST_VALUE(COUNT(DISTINCT user_id)) OVER (PARTITION BY cohort_month ORDER BY period), 1) AS retention_pct
FROM joined
GROUP BY cohort_month, period
ORDER BY cohort_month, period;


-- ─────────────────────────────────────────────────────────────
-- 8. NORTH STAR METRIC — Weekly Active Paying Users (WAPU)
-- ─────────────────────────────────────────────────────────────
SELECT
    strftime('%Y-W%W', event_date) AS week,
    COUNT(DISTINCT user_id)        AS weekly_paying_users
FROM events
WHERE event = 'paying'
GROUP BY 1
ORDER BY 1;


-- ─────────────────────────────────────────────────────────────
-- 9. REVENUE — MRR by month and plan
-- ─────────────────────────────────────────────────────────────
SELECT
    strftime('%Y-%m', e.event_date) AS month,
    u.plan,
    COUNT(DISTINCT e.user_id)       AS paying_users,
    ROUND(SUM(e.revenue), 2)        AS mrr
FROM events e
JOIN users u ON e.user_id = u.user_id
WHERE e.event = 'paying'
GROUP BY 1, 2
ORDER BY 1, 2;


-- ─────────────────────────────────────────────────────────────
-- 10. ACQUISITION CHANNEL PERFORMANCE
-- ─────────────────────────────────────────────────────────────
SELECT
    u.channel,
    COUNT(DISTINCT u.user_id)                                              AS total_signups,
    COUNT(DISTINCT CASE WHEN e.event='paying' THEN e.user_id END)          AS paying_users,
    ROUND(COUNT(DISTINCT CASE WHEN e.event='paying' THEN e.user_id END)
          * 100.0 / COUNT(DISTINCT u.user_id), 1)                         AS conversion_pct,
    ROUND(SUM(CASE WHEN e.event='paying' THEN e.revenue ELSE 0 END), 2)   AS total_revenue
FROM users u
LEFT JOIN events e ON u.user_id = e.user_id
GROUP BY u.channel
ORDER BY total_revenue DESC;


-- ─────────────────────────────────────────────────────────────
-- 11. WHAT'S GOING WRONG — Users who signed up but never activated
-- ─────────────────────────────────────────────────────────────
SELECT
    u.user_id,
    u.signup_date,
    u.channel,
    u.country,
    u.plan,
    CASE
        WHEN e.user_id IS NULL THEN 'Never Activated'
        ELSE 'Activated'
    END AS status
FROM users u
LEFT JOIN (
    SELECT DISTINCT user_id FROM events WHERE event = 'activation'
) e ON u.user_id = e.user_id
ORDER BY u.signup_date;


-- ─────────────────────────────────────────────────────────────
-- 12. AVERAGE SESSION DURATION by event type
-- ─────────────────────────────────────────────────────────────

SELECT
    session_id,
    user_id,
    MIN(event_ts) AS session_start,
    MAX(event_ts) AS session_end,
    (
        julianday(
            substr(MAX(event_ts),7,4) || '-' ||
            substr(MAX(event_ts),4,2) || '-' ||
            substr(MAX(event_ts),1,2) || ' ' ||
            substr(MAX(event_ts),12)
        )
        -
        julianday(
            substr(MIN(event_ts),7,4) || '-' ||
            substr(MIN(event_ts),4,2) || '-' ||
            substr(MIN(event_ts),1,2) || ' ' ||
            substr(MIN(event_ts),12)
        )
    ) * 24 * 60 AS duration_minutes
FROM events
GROUP BY session_id, user_id;