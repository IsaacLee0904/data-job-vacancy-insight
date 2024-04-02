import os, sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utils.log_utils import set_logger
from utils.database_utils import DatabaseConnector, DatabaseOperation

def main():
    logger = set_logger()
    connector = DatabaseConnector(logger)
    connection = connector.connect_to_db('datawarehouse')
    db_operation = DatabaseOperation(connection, logger)

    try:
        # Assuming 'source_data.job_listings_104' is the table you want to fetch data from
        df = db_operation.fetch_data('source_data.job_listings_104')
        if df is not None and not df.empty:
            logger.info(f"Retrieved {len(df)} rows from the database.")
            # Now you can process the DataFrame `df` as needed
        else:
            logger.warning("No data retrieved or table is empty.")
    except Exception as e:
        logger.error(f"An error occurred during data retrieval: {e}")
    finally:
        if connection:
            connection.close()
            logger.info("Database connection closed.")
