import os, sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utils.log_utils import set_logger
from utils.etl_utils import read_json_to_df, convert_column_type
from utils.database_utils import DatabaseConnector, DatabaseOperation, create_rawdata_table

def main():

    logger = set_logger()
    
    try:
        create_rawdata_table(logger)
        connector = DatabaseConnector(logger)
        connection = connector.connect_to_db('datawarehouse')
        db_operation = DatabaseOperation(connection, logger)

        directory_path = '/app/data/raw_data/'

        # load data
        df = read_json_to_df(directory_path, logger)

        if df is not None:
            
            # transform data type 
            df = convert_column_type(df, 'job_title', str)
            df = convert_column_type(df, 'company_name', str)
            df = convert_column_type(df, 'salary', str)
            df = convert_column_type(df, 'location', str)
            df = convert_column_type(df, 'job_description', str)
            df = convert_column_type(df, 'job_type', str)
            df = convert_column_type(df, 'degree_required', str)
            df = convert_column_type(df, 'major_required', str)
            df = convert_column_type(df, 'experience', str)
            df = convert_column_type(df, 'skill', str)
            df = convert_column_type(df, 'tools', str)
            df = convert_column_type(df, 'others', str)
            df = convert_column_type(df, 'url', str)
            df = convert_column_type(df, 'crawl_date', 'datetime', '%Y%m%d')
            # create uniqule key to aviod duplicate insert 
            df['unique_col'] = df['job_title'] + '_' + df['crawl_date'].astype(str)

            # insert data
            db_operation.insert_data('source_data.job_listings_104', df, 'unique_col')
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
