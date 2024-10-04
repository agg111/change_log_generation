import psycopg2

# We use the dbname, user, and password that we specified above
conn = psycopg2.connect(dbname="ajttd964b1", user="uk5vsrwdus0", password="Dbpassword123", host="free.lantern.dev", port="6432")

cursor = conn.cursor()
create_table_query = "CREATE TABLE small_world (id integer, vector real[3]);"
cursor.execute(create_table_query)
conn.commit()
cursor.close()

cursor = conn.cursor()

# Let's insert a vector [0,0,0] with id 0 (note that postgres uses {} braces)
cursor.execute("INSERT INTO small_world (id, vector) VALUES (0, '{0, 0, 0}');")

# Now let's insert some more vectors
v1 = [0, 0, 1]
v2 = [0, 1, 1]
v3 = [1, 1, 1]
v4 = [2, 0, 1]

cursor.execute("INSERT INTO small_world (id, vector) VALUES (%s, %s), (%s, %s), (%s, %s), (%s, %s);", (1, v1, 2, v2, 3, v3, 4, v4))

conn.commit()
cursor.close()

cursor = conn.cursor()

cursor.execute("CREATE INDEX ON small_world USING lantern_hnsw (vector);")

# We can also specify additional parameters to the index like this:
"""CREATE INDEX ON small_world USING lantern_hnsw (vector dist_l2sq_ops)
WITH
(M=2, ef_construction=10, ef=4, dim=3);"""

conn.commit()
cursor.close()

cursor = conn.cursor()

# We only need to set this at the beginning of a session
cursor.execute("SET enable_seqscan = false;")
cursor.execute("SELECT id, l2sq_dist(vector, ARRAY[0,0,0]) AS dist, vector FROM small_world ORDER BY vector <-> ARRAY[0,0,0] LIMIT 3;")

record = cursor.fetchone()
while record:
    print(f"Vector {record[2]} with ID {record[0]} has a L2-squared distance of {record[1]} from [0,0,0]")
    record = cursor.fetchone()

cursor.close()

# Close the postgres connection
conn.close()
