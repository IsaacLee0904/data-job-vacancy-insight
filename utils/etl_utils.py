import os
import pandas as pd

def read_json_to_df(directory_path, logger):
    """
    Read the latest JSON file from a specified directory into a pandas DataFrame.

    Parameters:
    - directory_path (str): The path to the directory containing JSON files.
    - logger (logging.Logger): A Logger object used for logging information and errors.

    Returns:
    - pd.DataFrame: A DataFrame containing the contents of the latest JSON file.
    """
    logger.info(f"Reading the latest JSON file from {directory_path}")

    files = os.listdir(directory_path)

    json_files = [file for file in files if file.endswith('.json')]

    if not json_files:
        logger.warning("No JSON files found in the directory.")
        return None

    json_files.sort(reverse=True)
    latest_json_file = json_files[0]

    df = pd.read_json(os.path.join(directory_path, latest_json_file))

    logger.info(f"Successfully read {latest_json_file}")

    return df

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