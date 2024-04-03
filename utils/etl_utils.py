import os
import pandas as pd
import shutil

def read_json_to_df(directory_path, logger):
    """
    Read the latest JSON file from a specified directory and convert it to a pandas DataFrame.

    Parameters:
    - directory_path (str): The path to the directory containing JSON files.
    - logger (logging.Logger): A Logger object used for logging information and errors.

    Returns:
    - tuple: A tuple containing the DataFrame and the file path. The DataFrame contains the contents of the latest JSON file,
             and the file path is the path to this JSON file. Returns (None, None) if no JSON files are found.
    """
    logger.info(f"Reading the latest JSON file from {directory_path}")

    # Get all files in the directory
    files = os.listdir(directory_path)

    # Filter out JSON files
    json_files = [file for file in files if file.endswith('.json')]

    # If no JSON files are found, log a warning and return None, None
    if not json_files:
        logger.warning("No JSON files found in the directory.")
        return None, None

    # Sort the files to find the latest one
    json_files.sort(reverse=True)
    latest_json_file = json_files[0]

    # Read the JSON file into a DataFrame
    file_path = os.path.join(directory_path, latest_json_file)
    df = pd.read_json(file_path)

    logger.info(f"Successfully read {latest_json_file}")

    # Return the DataFrame and the path to the JSON file
    return df, file_path

def move_to_backup_folder(file_path, backup_folder):
    
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    
    shutil.move(file_path, os.path.join(backup_folder, os.path.basename(file_path)))

def convert_column_type(df, column_name, target_type, format=None):
    """
    Convert the data type of a specific column in the DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.
    - column_name (str): The name of the column to convert.
    - target_type (type): The target data type.
    - format (str, optional): The format string if converting to datetime.

    Returns:
    - pd.DataFrame: The DataFrame with the converted column.
    """
    if target_type == 'datetime':
        df[column_name] = pd.to_datetime(df[column_name], format=format)
    else:
        df[column_name] = df[column_name].astype(target_type)
    
    return df