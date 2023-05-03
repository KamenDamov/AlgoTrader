#Script to remove duplicates
import psycopg2

query = """
-- create a temporary table with unique values
CREATE TEMPORARY TABLE temp_table AS 
SELECT DISTINCT * FROM your_table_name;

-- delete the original table
DROP TABLE your_table_name;

-- rename the temporary table to the original table name
ALTER TABLE temp_table RENAME TO your_table_name;
"""