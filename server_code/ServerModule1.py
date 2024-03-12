import anvil.server
import anvil.server
from pymongo import MongoClient
import re
import anvil.server
from pymongo import MongoClient
import re

@anvil.server.callable
def connect_to_mongodb(connString):
  # Here you would replace 'Your IP validation regex here' with your actual regex for IP validation
  
  client = MongoClient(connString)
  # Example: Attempt to list databases as a test of the connection
  db_list = client.list_database_names()
  return True, "Connection Successful, Databases: " + ", ".join(db_list)


# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

