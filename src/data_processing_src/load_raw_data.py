import os, sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utils.log_utils import set_logger
from utils.etl_utils import GeneralDataProcessor
from utils.database_utils import DatabaseConnector, DatabaseOperation, create_rawdata_table

def main():

    # setup logger
    logger = set_logger()
    
    try:
        create_rawdata_table(logger)
        connector = DatabaseConnector(logger)
        connection = connector.connect_to_db('datawarehouse')
        db_operation = DatabaseOperation(connection, logger)
        
        # setup configure
        directory_path = '/app/data/raw_data/'
        backup_folder_path = '/app/data/backup/'

        # load data
        df, file_path = GeneralDataProcessor.read_json_to_df(directory_path, logger)

        if df is not None and file_path:
            
            # transform data type 
            df = GeneralDataProcessor.convert_column_type(df, 'job_title', str)
            df = GeneralDataProcessor.convert_column_type(df, 'company_name', str)
            df = GeneralDataProcessor.convert_column_type(df, 'salary', str)
            df = GeneralDataProcessor.convert_column_type(df, 'location', str)
            df = GeneralDataProcessor.convert_column_type(df, 'job_description', str)
            df = GeneralDataProcessor.convert_column_type(df, 'job_type', str)
            df = GeneralDataProcessor.convert_column_type(df, 'degree_required', str)
            df = GeneralDataProcessor.convert_column_type(df, 'major_required', str)
            df = GeneralDataProcessor.convert_column_type(df, 'experience', str)
            df = GeneralDataProcessor.convert_column_type(df, 'skill', str)
            df = GeneralDataProcessor.convert_column_type(df, 'tools', str)
            df = GeneralDataProcessor.convert_column_type(df, 'others', str)
            df = GeneralDataProcessor.convert_column_type(df, 'url', str)
            df = GeneralDataProcessor.convert_column_type(df, 'crawl_date', 'datetime', '%Y%m%d')
            # create uniqule key to aviod duplicate insert 
            df['unique_col'] = df['job_title'] + '_' + df['crawl_date'].astype(str)

            # insert data
            db_operation.insert_data('source_data.job_listings_104', df, 'unique_col')

            # move the file to backup folder
            if file_path:
                GeneralDataProcessor.move_to_backup_folder(file_path, backup_folder_path)
                logger.info(f"Moved {os.path.basename(file_path)} to {backup_folder_path}")

        else:
            logger.warning("No data to insert.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    finally:
        if 'connection' in locals() and connection:
            connection.close()
            logger.info("Database connection closed.")

if __name__ == "__main__":
    main()
