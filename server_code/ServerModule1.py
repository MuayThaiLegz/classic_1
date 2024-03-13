#server.py

import anvil.server
from pymongo import MongoClient
import pandas as pd
from io import BytesIO
import re
from functools import lru_cache
import calendar
from data_processing import process_datafile, clean_column_names, identify_datetime_cols, convert_to_datetime, create_features

@anvil.server.callable
def connect_to_mongodb(connString):
    """
    Attempts to connect to MongoDB with the provided connection string.
    Returns a success status and message.
    """
    try:
        client = MongoClient(connString)
        client.admin.command('ping')
        client.close()
        return True, "Connected successfully."
    except Exception as e:
        return False, f"Connection failed: {str(e)}"

@anvil.server.callable
def get_verticals(connString):
    """
    Retrieves the list of databases and their collections.
    """
    try:
        client = MongoClient(connString)
        verticals = {db: client[db].list_collection_names() for db in client.list_database_names() if db not in ['admin', 'local', 'config']}
        client.close()
        return True, verticals
    except Exception as e:
        return False, f"Failed to get verticals: {str(e)}"


def sanitize_name(name):
    """Sanitize database or collection name."""
    return re.sub(r'[.\s]', '_', name)

@anvil.server.background_task
def store_data(db_name, collection_name, file, connString):
    """
    Stores the data from the uploaded file into the specified MongoDB collection.
    """
    try:
        # Ensure file is not None and has a content_type
        if not file or not hasattr(file, 'content_type'):
            return False, "No file or file type provided."

        sanitized_db_name = sanitize_name(db_name)
        sanitized_collection_name = sanitize_name(collection_name)

        client = MongoClient(connString)
        db = client[sanitized_db_name]
        collection = db[sanitized_collection_name]
        
        # Read file into DataFrame
        file_like_object = BytesIO(file.get_bytes())
        if file.content_type == 'text/csv':
            df = pd.read_csv(file_like_object)
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(file_like_object)
        elif file.content_type == 'application/json':
            df = pd.read_json(file_like_object)
        else:
            return False, "Unsupported file type."

        # Process and store the DataFrame
        processed_df, _, _, _, _, _, _ = process_datafile(df)
        records = processed_df.to_dict('records')
        collection.insert_many(records)
        client.close()
        return True, f"Data saved successfully in {sanitized_db_name}/{sanitized_collection_name}."
    except Exception as e:
        return False, f"Failed to store data: {str(e)}"

@anvil.server.callable
def initiate_file_processing(file, db_name, collection_name, connString):
    anvil.server.launch_background_task('store_data', file, db_name, collection_name, connString)
    return "Processing started"
  
