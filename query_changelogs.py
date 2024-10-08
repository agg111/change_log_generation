import psycopg2
from sentence_transformers import SentenceTransformer
import torch

CHANGE_LOGS_TABLE_NAME = "changelogs"

conn = psycopg2.connect(dbname="ajttd964b1", user="uk5vsrwdus0", password="Dbpassword123", host="free.lantern.dev", port="6432")

device = 'cuda' if torch.cuda.is_available() else 'cpu'
if device != 'cuda':
    print(f"You are using {device}. This is much slower than using "
          "a CUDA-enabled GPU. If on Colab you can change this by "
          "clicking Runtime > Change runtime type > GPU.")
    
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

# query = 'What release improves caching for next.js?'
query = "What releases are related to CacheStore updates?"

embedded_query = model.encode(query)
embedded_query = [float(x) for x in embedded_query]

cursor = conn.cursor()

# We only need to set this at the beginning of a session
cursor.execute("SET enable_seqscan = false;")
cursor.execute(f"SELECT content, cos_dist(vector, ARRAY{embedded_query}) AS dist FROM {CHANGE_LOGS_TABLE_NAME} ORDER BY vector <-> ARRAY{embedded_query} LIMIT 5;")

record = cursor.fetchone()
print("=== RECORDS === ")
# print(record)
while record:
    print(f"{record[0]}  (dist: {record[1]})")
    record = cursor.fetchone()

cursor.close()

# Close the postgres connection
conn.close()