import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

# server_code.py

import anvil.server
from pymongo import MongoClient
import pandas as pd
from io import BytesIO

@anvil.server.callable
def connect_to_mongodb(connString):
    try:
        client = MongoClient(connString)
        client.admin.command('ping')
        # Close the client after checking the connection
        client.close()
        return True, "Connected successfully.", connString
    except Exception as e:
        return False, f"Connection failed: {str(e)}", None

@anvil.server.callable
def get_verticals(connString):
    try:
        client = MongoClient(connString)
        verticals = {}
        db_names = client.list_database_names()
        for db_name in db_names:
            if db_name not in ['admin', 'local', 'config', 'Modelsdb', 'dev_db', 'document_embeddings', 'Models_evaluation']:
                verticals[db_name] = client[db_name].list_collection_names()
        client.close()
        return True, verticals
    except Exception as e:
        return False, f"Failed to get verticals: {str(e)}"

@anvil.server.callable
def process_and_load_file(file, connString):
    try:
        client = MongoClient(connString)
        file_like_object = BytesIO(file.get_bytes())
        
        if file.content_type == 'text/csv':
            df = pd.read_csv(file_like_object)
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(file_like_object)
        elif file.content_type == 'application/json':
            df = pd.read_json(file_like_object)
        
        uploaded_fileName = file.name.rsplit('.', 1)[0]
        db = client['AnvilVille']
        collection = db[uploaded_fileName]
        collection.insert_many(df.to_dict('records'))
        client.close()
        return True, f"Data saved successfully in {uploaded_fileName}."
    except Exception as e:
        return False, f"Failed to process file: {str(e)}"
