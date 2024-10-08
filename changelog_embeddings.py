from sentence_transformers import SentenceTransformer
import torch

import utils

import psycopg2
from tqdm.auto import tqdm

conn = psycopg2.connect(dbname="ajttd964b1", user="uk5vsrwdus0", password="Dbpassword123", host="free.lantern.dev", port="6432")

cursor = conn.cursor()

CHANGE_LOGS_TABLE_NAME = "changelogs"
# create_table_query = "CREATE TABLE changelogs (id serial PRIMARY key, content text, vector real[]);"

# cursor.execute(create_table_query)

# conn.commit()

device = 'cuda' if torch.cuda.is_available() else 'cpu'
if device != 'cuda':
    print(f"You are using {device}. This is much slower than using "
          "a CUDA-enabled GPU. If on Colab you can change this by "
          "clicking Runtime > Change runtime type > GPU.")

model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

change_logs = utils.fetch_changelog()

for i in tqdm(range(0, len(change_logs))):
    content = change_logs[i]

    # Create embedding for the question
    vector = [float(x) for x in model.encode(change_logs[i])]

    # Insert the content of the question as well as the embedding into our db
    cursor.execute(f"INSERT INTO {CHANGE_LOGS_TABLE_NAME} (content, vector) VALUES (%s, %s);", (content, vector))

conn.commit()

cursor.execute(f"CREATE INDEX ON {CHANGE_LOGS_TABLE_NAME} USING lantern_hnsw (vector dist_cos_ops) WITH (dim=384);")

cursor.close()

conn.commit()
conn.close()