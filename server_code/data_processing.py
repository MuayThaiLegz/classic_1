# data_processing.py


import pandas as pd
import numpy as np
import re
from functools import lru_cache
import calendar

def clean_column_names(columns):
    """Simplify column names using regex and split methods."""
    pattern = r'filtered/application/\d+/device/[^/]+/event/up\.(.+)'
    cleaned_columns = []

    for col in columns:
        match = re.search(pattern, col)
        col = match.group(1) if match else col.split("/")[-1]
        col = col.split('.', 1)[-1] if '.' in col else col
        cleaned_columns.append(col)

    return cleaned_columns

def identify_datetime_cols(df, datetime_keywords):
    """Identify potential datetime columns in the DataFrame."""
    datetime_cols = [col for col in df.columns if any(keyword in col for keyword in datetime_keywords) or df[col].dtype == 'object']
    return datetime_cols

def convert_to_datetime(df, datetime_cols):
    """Convert identified columns to datetime format."""
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        df[col] = df[col].dt.strftime('%Y-%m-%d-%H:%M:%S') if not df[col].isnull().all() else df[col]
    return df

def create_features(df, date_col):
    """Generate time-based features from the datetime column."""
    df['season'] = df[date_col].dt.month % 12 // 3 + 1
    df['time_of_day'] = pd.cut(df[date_col].dt.hour, [0, 6, 12, 18, 24], labels=['Night', 'Morning', 'Afternoon', 'Evening'], right=False)
    df['day_of_week'] = df[date_col].dt.day_name().str.lower()
    df['month'] = df[date_col].dt.month_name().str.lower()
    df['hour'] = df[date_col].dt.hour
    return df


def process_datafile(df):
    datetime_keywords = set(['rx.ts', 'info.datecreated', 'date', 'time',
                        'iothubenqueuedtime' 'timestamp', 'utc', 'published',
                        'publishedat','payload.publishedat', 'datecreated',
                        'payload.timestamp', 'noted_date', 'created_at',
                        'updated_at', 'modified', 'expires', 'expiry_date',
                        'accessed_at', 'deleted_at', 'published_on', 'event_time',
                        'transaction_time', 'log_time', 'start_date', 'start_time', 'end_date', 
                        'end_time', 'recorded_at', 'received_at', 'sent_at'])
    date_pattern = r'(?:\d{1,2}[-/]\d{1,2}[-/]\d{4})|(?:\d{4}[-/]\d{1,2}[-/]\d{1,2})'
  
  
    # Clean column names
    df.columns = clean_column_names(df.columns)

    # Identify and convert datetime columns
    datetime_cols = identify_datetime_cols(df, datetime_keywords)
    df = convert_to_datetime(df, datetime_cols)

    # Assume the first datetime column is the main datetime column
    main_datetime_col = datetime_cols[0] if datetime_cols else None

    # Drop unwanted columns
    columns_to_drop = ['_id', 'index', 'Unnamed: 0', 'level_0']
    df = df.drop(columns=columns_to_drop, errors='ignore')

    # Create features based on the main datetime column
    if main_datetime_col:
        df = create_features(df, main_datetime_col)

    # Extract lists of latitude/longitude, numerical, and object columns
    lat_long_list = [col for col in df.columns if col in ['latitude', 'longitude']]
    numerical_data = df.select_dtypes(include=np.number)
    object_data = df.select_dtypes(include='object')

    numerical_options_list = numerical_data.columns.difference(lat_long_list)
    object_options_list = object_data.columns.difference(['deviceid', 'devicetype', 'gatewayid', 'status'])

    return df, lat_long_list, numerical_data, numerical_options_list, object_data, object_options_list, main_datetime_col

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
def clean_column_names(columns):
    """
    Cleans column names using a predefined pattern.
    """
    pattern = r'filtered/application/\d+/device/[^/]+/event/up\.(.+)'
    cleaned_columns = []
    for col in columns:
        match = re.search(pattern, col)
        col = match.group(1) if match else col.split('/')[-1]
        col = col.split('.', 1)[-1] if '.' in col else col
        cleaned_columns.append(col)
    return cleaned_columns

def identify_datetime_cols(df, datetime_keywords):
    """
    Identifies columns that are likely to be datetime based on their names.
    """
    datetime_cols = [col for col in df.columns if any(keyword in col for keyword in datetime_keywords) or df[col].dtype == 'object']
    return datetime_cols

def process_datafile(df):
    """
    Processes the DataFrame to clean column names, identify datetime columns, and create additional features.
    """
    # Define keywords to identify datetime columns
    
    datetime_keywords = set(['rx.ts', 'info.datecreated', 'date', 'time',
                        'iothubenqueuedtime' 'timestamp', 'utc', 'published',
                        'publishedat','payload.publishedat', 'datecreated',
                        'payload.timestamp', 'noted_date', 'created_at',
                        'updated_at', 'modified', 'expires', 'expiry_date',
                        'accessed_at', 'deleted_at', 'published_on', 'event_time',
                        'transaction_time', 'log_time', 'start_date', 'start_time', 'end_date', 
                        'end_time', 'recorded_at', 'received_at', 'sent_at'])
  
    df.columns = clean_column_names(df.columns)
    datetime_cols = identify_datetime_cols(df, datetime_keywords)
    df = convert_to_datetime(df, datetime_cols)

    main_datetime_col = datetime_cols[0] if datetime_cols else None
    if main_datetime_col:
        df = create_features(df, main_datetime_col)

    lat_long_list, numerical_data, numerical_options_list, object_data, object_options_list = [], [], [], [], []
    return df, lat_long_list, numerical_data, numerical_options_list, object_data, object_options_list, main_datetime_col

def convert_to_datetime(df, datetime_cols):
    """
    Converts identified columns to datetime format.
    """
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S') if not df[col].isnull().all() else df[col]
    return df

def create_features(df, date_col):
    """
    Creates additional time-based features from the specified datetime column.
    """
    df['season'] = df[date_col].dt.month % 12 // 3 + 1
    df['time_of_day'] = pd.cut(df[date_col].dt.hour, bins=[0, 6, 12, 18, 24], labels=['Night', 'Morning', 'Afternoon', 'Evening'], right=False)
    df['day_of_week'] = df[date_col].dt.day_name().str.lower()
    df['month'] = df[date_col].dt.month_name().str.lower()
    df['hour'] = df[date_col].dt.hour
    return df
