# server_code.py

import anvil.server
from pymongo import MongoClient
import pandas as pd
from io import BytesIO

@anvil.server.callable
def connect_to_mongodb(connString):
    try:
        global client
        client = MongoClient(connString)
        client.admin.command('ping')
        return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False

@anvil.server.callable
def get_verticals():
    verticals = {}
    if 'client' not in globals():
        return {}
    db_names = client.list_database_names()
    for db_name in db_names:
        if db_name not in ['admin', 'local', 'config', 'Modelsdb', 'dev_db', 'document_embeddings', 'Models_evaluation']:
            verticals[db_name] = client[db_name].list_collection_names()
    return verticals


@anvil.server.callable
def process_and_load_file(file, connString):
    try:
        # Convert bytes to a file-like object
        file_like_object = BytesIO(file.get_bytes())

        # Determine the file type and load accordingly
        if file.content_type == 'text/csv':
            df = pd.read_csv(file_like_object)
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(file_like_object)
        elif file.content_type == 'application/json':
            df = pd.read_json(file_like_object)
        # Add more elif blocks for other content types if necessary
        
        # Example process and load data into MongoDB (simplified)
        client = MongoClient(connString)
        uploaded_fileName = file.name.replace('.csv', '')
        db = client['AnvilVille']
        collection = db[f'{uploaded_fileName}']
        # Convert DataFrame to dictionary and insert into MongoDB
        collection.insert_many(df.to_dict('records'))
        
        return True  # Indicate success
    except Exception as e:
        print(f"Failed to process file: {str(e)}")
        return False

