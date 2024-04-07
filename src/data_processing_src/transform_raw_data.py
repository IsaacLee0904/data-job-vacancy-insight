import os, sys
import datetime

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utils.log_utils import set_logger
from utils.database_utils import DatabaseConnector, DatabaseOperation, create_stagedata_table
from utils.etl_utils import GeneralDataProcessor, RawDataProcessor

def main():
    
    # setup logger
    logger = set_logger()

    # create instances of processors
    raw_data_processor = RawDataProcessor(logger)

    # connect to database
    connector = DatabaseConnector(logger)
    connection = connector.connect_to_db('datawarehouse')
    db_operation = DatabaseOperation(connection, logger)
    # create stage data table for inserting transform data
    create_stagedata_table(logger)

    try:
        # set condition to fetch data from source_data database
        today_date = datetime.datetime.today().strftime('%Y-%m-%d')
        condition = f"crawl_date = '{today_date}'"
        df = db_operation.fetch_data('source_data.job_listings_104', "crawl_date = '2024-04-01'") # need to change to condition while everything get ready!
        
        # data transform rules
        if df is not None and not df.empty:
            logger.info(f"Retrieved {len(df)} rows from the database.")
            # set up a job title keywords for data cleaning            
            title_keywords = ['數據', '資料', '機器學習', 'Data', 'AI', 
                             'Machine Learning', '演算法', '分析', 'NLP',
                             'BI', 'Business Analyst']
            # set up a job type keywords for data cleaning 
            type_keywords = ['軟體工程師', '演算法工程師', '系統分析師', '資料庫管理人員', '其他資訊專業人員', 
                        '數據分析師', '資料工程師', '市場調查／市場分析', 'Internet程式設計師', '系統工程師', 
                        '資料科學家', '其他專案管理師', '軟體專案管理師', '統計學研究員', 'AI工程師',
                        '統計精算人員', '網路管理工程師', '營運管理師／系統整合／ERP專案師', '網站行銷企劃'
                        '專案經理', '雲端工程師', '軟體工程研發高階主管', '顧問師']
                        
            # Filter the DataFrame based on job title and job type
            df_filtered = raw_data_processor.filter_jobs_by_title_and_type(df, title_keywords, type_keywords)
            logger.info(f"Filtered down to {len(df_filtered)} rows based on keywords.")
            # Add county column to deal with location 
            df_filtered = df_filtered.copy() # to avoid warnings about SettingWithCopyWarning
            df_filtered = raw_data_processor.process_location(df_filtered)
            # Convert multi-string type columns into a list
            df_filtered = raw_data_processor.convert_to_list(df_filtered, ['job_type', 'degree_required', 'major_required', 'skill', 'tools']) 
            # Transform data type           
            df_filtered = GeneralDataProcessor.convert_column_type(df_filtered, 'job_title', str)
            df_filtered = GeneralDataProcessor.convert_column_type(df_filtered, 'company_name', str)
            df_filtered = GeneralDataProcessor.convert_column_type(df_filtered, 'salary', str)
            df_filtered = GeneralDataProcessor.convert_column_type(df_filtered, 'location', str)
            df_filtered = GeneralDataProcessor.convert_column_type(df_filtered, 'job_description', str)
            df_filtered = GeneralDataProcessor.convert_column_type(df_filtered, 'experience', str)
            df_filtered = GeneralDataProcessor.convert_column_type(df_filtered, 'others', str)
            df_filtered = GeneralDataProcessor.convert_column_type(df_filtered, 'url', str)
            df_filtered = GeneralDataProcessor.convert_column_type(df_filtered, 'crawl_date', 'datetime', '%Y-%m-%d')
            df_filtered = GeneralDataProcessor.convert_column_type(df_filtered, 'unique_col', str)
            df_filtered = GeneralDataProcessor.convert_column_type(df_filtered, 'county', str)
            # reorder the columns in dataframe
            df_filtered = df_filtered[['id', 'job_title', 'company_name', 'salary', 'county', 
                                       'location', 'job_description', 'job_type', 'degree_required', 'major_required',
                                       'experience', 'skill', 'tools', 'others', 'url', 
                                       'crawl_date', 'unique_col']]
            logger.info('Successfully transformed raw data.')

            if df_filtered is not None:
                # insert data
                db_operation.insert_data('staging_data.job_listings_104', df_filtered, 'unique_col')
            
            else:
                logger.warning("No data to insert.")
            
        else:
            logger.warning("No data retrieved or table is empty.")

    except Exception as e:
        logger.error(f"An error occurred during data retrieval: {e}")

    finally:
        if connection:
            connection.close()
            logger.info("Database connection closed.")
        
if __name__ == "__main__":
    main()
