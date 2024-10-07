from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import torch

import psycopg2
from tqdm.auto import tqdm


dataset = load_dataset('quora', split='train[100000:150000]')
print(type(dataset))
# Some example samples of this dataset
dataset[:4]

questions = []

for record in dataset['questions']:
    questions.extend(record['text'])

# Remove duplicates
questions = list(set(questions))
print('\n'.join(questions[:4]))
print(f"Number of questions: {len(questions)}")

device = 'cuda' if torch.cuda.is_available() else 'cpu'
if device != 'cuda':
    print(f"You are using {device}. This is much slower than using "
          "a CUDA-enabled GPU. If on Colab you can change this by "
          "clicking Runtime > Change runtime type > GPU.")

model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

conn = psycopg2.connect(dbname="ajttd964b1", user="uk5vsrwdus0", password="Dbpassword123", host="free.lantern.dev", port="6432")

# Create the table
cursor = conn.cursor()

create_table_query = "CREATE TABLE questions (id serial PRIMARY key, content text, vector real[]);"

cursor.execute(create_table_query)

conn.commit()
cursor.close()


cursor = conn.cursor()

# The questions we want to embed
# To make this faster, we will only insert the first 1000 questions
Qs = questions[:1000]

for i in tqdm(range(0, len(Qs))):
    content = Qs[i]

    # Create embedding for the question
    vector = [float(x) for x in model.encode(Qs[i])]

    # Insert the content of the question as well as the embedding into our db
    cursor.execute("INSERT INTO questions (content, vector) VALUES (%s, %s);", (content, vector))

conn.commit()
cursor.close()

cursor = conn.cursor()

cursor.execute("CREATE INDEX ON questions USING lantern_hnsw (vector dist_cos_ops) WITH (dim=384);")

conn.commit()
cursor.close()

query = 'How do I become a better software engineer?'

embedded_query = model.encode(query)
embedded_query = [float(x) for x in embedded_query]

cursor = conn.cursor()

# We only need to set this at the beginning of a session
cursor.execute("SET enable_seqscan = false;")
cursor.execute(f"SELECT content, cos_dist(vector, ARRAY{embedded_query}) AS dist FROM questions ORDER BY vector <-> ARRAY{embedded_query} LIMIT 5;")

record = cursor.fetchone()
print("=== RECORDS === ")
# print(record)
while record:
    print(f"{record[0]}  (dist: {record[1]})")
    record = cursor.fetchone()

cursor.close()

# Close the postgres connection
conn.close()