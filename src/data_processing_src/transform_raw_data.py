import os, sys
import datetime

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utils.log_utils import set_logger
from utils.database_utils import DatabaseConnector, DatabaseOperation, create_stagedata_table
from utils.etl_utils import GeneralDataProcessor, RawDataProcessor

def connect_to_database(logger):
    """
    Establish a connection to the database and return the connector and operation objects.
    """
    connector = DatabaseConnector(logger)
    connection = connector.connect_to_db('datawarehouse')
    db_operation = DatabaseOperation(connection, logger)
    logger.info("Connected to the database successfully.")
    return connection, db_operation

def create_and_filter_data(db_operation, logger):
    """
    Create the staging data table, fetch data, and apply filters based on job titles, types, and locations.
    """
    create_stagedata_table(logger)
    logger.info("Stage data table created or verified.")

    today_date = datetime.datetime.today().strftime('%Y-%m-%d')
    condition = f"crawl_date = '{today_date}'"
    df = db_operation.fetch_data('source_data.job_listings_104', "crawl_date = '2024-04-01'")
    # df = db_operation.fetch_data('source_data.job_listings_104', condition)
    logger.info(f"Fetched data for the date: {today_date} with {len(df)} rows (if not empty).")

    if df is not None and not df.empty:
        logger.info(f"Retrieved {len(df)} rows from the database for processing.")
        raw_data_processor = RawDataProcessor(logger)    
        df_filtered = raw_data_processor.filter_jobs_by_title_and_type(df)
        df_filtered = df_filtered.copy()
        df_filtered = raw_data_processor.classify_data_role(df_filtered)
        df_filtered = raw_data_processor.process_location(df_filtered)
        df_filtered = raw_data_processor.convert_to_list(df_filtered, ['job_type', 'degree_required', 'major_required', 'skill', 'tools']) 
        
        for column in ['data_role', 'job_title', 'company_name', 'salary', 'location', 'job_description', 'experience', 'others', 'url', 'county']:
            df_filtered = GeneralDataProcessor.convert_column_type(df_filtered, column, str)
        df_filtered = GeneralDataProcessor.convert_column_type(df_filtered, 'crawl_date', 'datetime', '%Y-%m-%d')
        df_filtered = GeneralDataProcessor.convert_column_type(df_filtered, 'unique_col', str)

        logger.info(f"Data processed and filtered down to {len(df_filtered)} rows.")
        return df_filtered
    else:
        logger.warning("No data retrieved or the table is empty.")
        return None

def main():
    
    # setup logger
    logger = set_logger()

    # connect to database
    connection, db_operation = connect_to_database(logger)
    df_filtered = create_and_filter_data(db_operation, logger)
        
    if df_filtered is not None and not df_filtered.empty:
        db_operation.insert_data('staging_data.job_listings_104', df_filtered, 'unique_col')
        logger.info(f"Inserted {len(df_filtered)} rows into staging_data.job_listings_104.")
    else:
        logger.warning("No data to insert into the staging database.")

    if connection:
        connection.close()
        logger.info("Database connection closed.")
        
if __name__ == "__main__":
    main()
