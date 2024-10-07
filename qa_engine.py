import csv
import pandas as pd
import psycopg2

from towhee import pipe, ops
import numpy as np
from towhee.datacollection import DataCollection


df = pd.read_csv('question_answer.csv')
print(df.head())

conn = psycopg2.connect(dbname="ajttd964b1", user="uk5vsrwdus0", password="Dbpassword123", host="free.lantern.dev", port="6432")

# Create the table
cursor = conn.cursor()

TABLE_NAME = "questions_answers"
create_table_query = f"CREATE TABLE {TABLE_NAME} (id integer, question text, answer text, vector real[]);"

cursor.execute(create_table_query)

conn.commit()
cursor.close()


# Define the processing pipeline
def insert_row(id, vec, question, answer):
    vector = [float(x) for x in vec]
    cursor.execute(f"INSERT INTO {TABLE_NAME} (id, question, answer, vector) VALUES (%s, %s, %s, %s);", (id, question, answer, vector))
    return True

insert_pipe = (
    pipe.input('id', 'question', 'answer')
        .map('question', 'vec', ops.text_embedding.dpr(model_name='facebook/dpr-ctx_encoder-single-nq-base'))
        # We normalize the embedding here
        .map('vec', 'vec', lambda x: x / np.linalg.norm(x, axis=0))
        .map(('id', 'vec', 'question', 'answer'), 'insert_status', insert_row)
        .output()
)

# Compute embeddings and insert data
cursor = conn.cursor()

with open('question_answer.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        insert_pipe(*row)

conn.commit()
cursor.close()

# Create index using lantern
cursor = conn.cursor()

cursor.execute(f"CREATE INDEX ON {TABLE_NAME} USING lantern_hnsw (vector dist_l2sq_ops) WITH (dim=768);")

conn.commit()
cursor.close()


# Perform search
conn.rollback()
cursor = conn.cursor()

# We only need to set this at the beginning of a session
cursor.execute("SET enable_seqscan = false;")
conn.commit()

def vector_search(vec):
  query_vector = str([float(x) for x in vec])
  cursor.execute(f"SELECT question AS similar_question, answer FROM {TABLE_NAME} ORDER BY vector <-> ARRAY{query_vector} LIMIT 1;")
  record = cursor.fetchall()[0]
  return record

ans_pipe = (
    pipe.input('question')
        .map('question', 'vec', ops.text_embedding.dpr(model_name="facebook/dpr-ctx_encoder-single-nq-base"))
        .map('vec', 'vec', lambda x: x / np.linalg.norm(x, axis=0))
        .map('vec', ('similar_question','answer'), vector_search)
        .output('question', 'similar_question', 'answer')
)

QUERY_QUESTION = "How much does disability insurance cost?"

ans = ans_pipe(QUERY_QUESTION)
ans = DataCollection(ans)
ans.show()

cursor.close()

# Close the postgres connection
conn.close()