# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import requests
import json
import os

# %%
DB_LOGIN = 'admin'        # os.getenv('COUCHDB_JDHP_SNIPPETS_USER')       # 'admin'
DB_PASSWORD = 'password'  # os.getenv('COUCHDB_JDHP_SNIPPETS_PASSWORD')   # 'password'
DB_ADDRESS = '127.0.0.1'
DB_PORT = '5984'

DB_URL = f'http://{DB_LOGIN}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}'
DB_NAME = 'my_db'
DB_VIEW = 'my_view'
DB_FILTER = 'my_filter'

auth = (DB_LOGIN, DB_PASSWORD)

# %% [markdown]
# ## Print general information about the server

# %%
# curl http://127.0.0.1:5984/
response = requests.get(f'{DB_URL}/')
print(response.text)

# %% [markdown]
# ## Delete a database

# %%
# curl -X DELETE http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@127.0.0.1:5984/plankton
response = requests.delete(f'{DB_URL}/{DB_NAME}')
print(response.text)

# %% [markdown]
# ## List all databases

# %%
# curl -X GET http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@127.0.0.1:5984/_all_dbs
response = requests.get(f'{DB_URL}/_all_dbs')
print(response.text)

# %% [markdown]
# ## Create a database

# %%
# curl -X PUT http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@127.0.0.1:5984/my_db
response = requests.put(f'{DB_URL}/{DB_NAME}')
print(response.text)

# %% [markdown]
# ## Push documents

# %%
# curl -X POST -H "Content-Type: application/json" http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@127.0.0.1:5984/my_db -d '{ "in" : {"i1":1, "i2":2}, "out": {"o1":1, "o2":2} }'
headers = {'Content-Type': 'application/json'}
data = json.dumps({"in" : {"i1":1, "i2":2}, "out": {"o1":1, "o2":2}})
response = requests.post(f'{DB_URL}/{DB_NAME}', headers=headers, data=data)
print(response.text)

# curl -X POST -H "Content-Type: application/json" http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@127.0.0.1:5984/my_db -d '{ "in" : {"i1":11, "i2":22}, "out": {"o1":11, "o2":22} }'
data = json.dumps({"in" : {"i1":11, "i2":22}, "out": {"o1":11, "o2":22}})
response = requests.post(f'{DB_URL}/{DB_NAME}', headers=headers, data=data)
print(response.text)

# %% [markdown]
# ## Fetch all documents of the database (at once)

# %% [markdown]
# This is adapted for small databases (i.e. if all documents fit in memory).

# %% [markdown]
# To retrieve documents from a CouchDB database one by one in a for loop, you can use the CouchDB _all_docs API with the include_docs=true option to retrieve all documents, then iterate over each document. Here are the steps in pseudocode:
#
# 1. Make a GET request to /_all_docs with the query parameter include_docs=true to get all documents.
# 2. Convert the response to JSON.
# 3. Access the list of documents via the rows key in the JSON.
# 4. Iterate over each item in the list.
# 5. For each item, access the document via the doc key.

# %%
# Fetch all documents
response = requests.get(f"{DB_URL}/{DB_NAME}/_all_docs?include_docs=true", auth=auth)
docs = response.json()

# Iterate on each document
for row in docs["rows"]:
    doc = row["doc"]
    print(doc)  # Do something with the document...


# %% [markdown]
# ## Fetch all documents of the database (one by one)

# %% [markdown]
# This is adapted for large databases (i.e. if all documents cannot fit in memory).

# %% [markdown]
# This code replaces bulk retrieval with a generator that iterates over each document in the database, using pagination to avoid memory issues. Use this generator in your code to process the documents one by one.

# %%
# Define a generator to fetch documents one by one
def fetch_docs_one_by_one(db_url, db_name, auth):
    startkey = None
    while True:
        params = {'include_docs': 'true', 'limit': 1}
        if startkey:
            params['startkey'] = json.dumps(startkey)
            params['skip'] = 1  # Skip the current startkey document

        response = requests.get(f'{db_url}/{db_name}/_all_docs', params=params, auth=auth)
        data = response.json()

        rows = data.get('rows', [])
        if not rows:
            break  # No more documents

        doc = rows[0].get('doc')
        yield doc

        startkey = doc['_id']

# Use the generator to fetch documents one by one
for doc in fetch_docs_one_by_one(DB_URL, DB_NAME, auth):
    print(doc)  # Do something with the document...

# %% [markdown]
# ## Query the database with a "view"

# %%
# C.f. https://docs.couchdb.org/en/stable/api/ddoc/index.html

# Create a view
# curl -X PUT http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@127.0.0.1:5984/my_db/_design/my_view -d '{"views":{"my_filter":{"map": "function(doc) { if(doc.in && doc.in.i1 && doc.out) { emit(doc.in.i1, doc.out); }}"}}}'
data = json.dumps({"views":{DB_FILTER:{"map": "function(doc) { if(doc.in && doc.in.i1 && doc.out) { emit(doc.in.i1, doc.out); }}"}}})
response = requests.put(f'{DB_URL}/{DB_NAME}/_design/{DB_VIEW}', headers=headers, data=data)
print(response.text)

# Query the view
# curl -X GET http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@127.0.0.1:5984/my_db/_design/my_view/_view/my_filter
response = requests.get(f'{DB_URL}/{DB_NAME}/_design/{DB_VIEW}/_view/{DB_FILTER}')
print(response.text)
print(response.json())

