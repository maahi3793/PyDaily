-- check_db_size.sql
-- Check the size of each table in your database including indexes.

SELECT
  table_name,
  (xpath('/row/cnt/text()', xml_count))[1]::text::int AS row_count,
  pg_size_pretty(table_size) AS table_size,
  pg_size_pretty(indexes_size) AS indexes_size,
  pg_size_pretty(total_size) AS total_size
FROM (
  SELECT
    table_name,
    table_schema,
    pg_total_relation_size(table_name::text) AS total_size,
    pg_relation_size(table_name::text) AS table_size,
    pg_indexes_size(table_name::text) AS indexes_size,
    query_to_xml(format('select count(*) as cnt from %I.%I', table_schema, table_name), false, true, '') as xml_count
  FROM information_schema.tables
  WHERE table_schema = 'public' -- Change to 'auth' to see auth tables if needed
) AS sizes
ORDER BY total_size DESC;
