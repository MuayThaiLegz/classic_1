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

import anvil.server
from pymongo import MongoClient
import pandas as pd
from io import BytesIO

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
        db = client['Cisco']
        collection = db['your_collection']
        # Convert DataFrame to dictionary and insert into MongoDB
        collection.insert_many(df.to_dict('records'))
        
        return True  # Indicate success
    except Exception as e:
        print(f"Failed to process file: {str(e)}")
        return False

# import anvil.server
# import anvil.server
# from pymongo import MongoClient
# import re
# import anvil.server
# from pymongo import MongoClient
# import re

# @anvil.server.callable
# def connect_to_mongodb(connString):
#     try:
#         client = MongoClient(connString)
#         # Perform a quick operation to validate the connection
#         client.admin.command('ping')
#         return True
#     except Exception as e:
#         print(f"Connection failed: {str(e)}")
#         return False

# @anvil.server.callable
# def get_verticals(connString):
#     verticals = {}
#     client = MongoClient(connString)
#     db_names = client.list_database_names()
#     for db_name in db_names:
#         if db_name not in ['admin', 'local', 'config','Modelsdb','dev_db','document_embeddings','Models_evaluation']:
#             verticals[db_name] = client[db_name].list_collection_names()
#     return verticals

# @anvil.server.callable
# def process_and_load_file(file):
#     import pandas as pd
    
#     if file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
#         # Assuming the file is an Excel file
#         df = pd.read_excel(file)
#     elif file.content_type == 'text/csv':
#         df = pd.read_csv(file)
#     # Add more conditions for other file types (.json, .parquet) as necessary

#     # Process the DataFrame 'df' as needed

#     # Example: Convert DataFrame to a list of dictionaries for MongoDB insertion
#     data_to_insert = df.to_dict('records')

#     # You would typically use a MongoDB connection here to insert data
#     # For simplicity, let's print the data to console
#     print(data_to_insert)

#     return True  # Indicate success


# # This is a server module. It runs on the Anvil server,
# # rather than in the user's browser.
# #
# # To allow anvil.server.call() to call functions here, we mark
# # them with @anvil.server.callable.
# # Here is an example - you can replace it with your own:
# #
# # @anvil.server.callable
# # def say_hello(name):
# #   print("Hello, " + name + "!")
# #   return 42
# #

