import sys, os
import datetime
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.log_utils import set_logger
from utils.database_utils import DatabaseConnector, DatabaseOperation

def connect_to_database(logger):
    """
    Establish a connection to the database and return the connector and operation objects.
    """
    connector = DatabaseConnector(logger)
    connection = connector.connect_to_db('datawarehouse')
    db_operation = DatabaseOperation(connection, logger)
    logger.info("Connected to the database successfully.")
    return connection, db_operation

class FetchReportData:
    def __init__(self, logger):
        """
        Initialize the FetchReportData object by establishing a connection to the database.
        """
        self.connection, self.db_operation = connect_to_database(logger)
        self.logger = logger

    def execute_query(self, query):
        """
        Execute a SQL query and return the results.
        """
        try:
            cursor = self.connection.cursor()  # Creating a new cursor as needed
            cursor.execute(query)
            result = cursor.fetchall()  # Fetch all the results
            cursor.close()  # Close the cursor after fetching data
            return result
        except Exception as e:
            self.logger.error(f"Failed to execute query {query}: {str(e)}")
            return None

    def fetch_all_tables(self):
        """
        Fetch all tables from the 'reporting_data' schema.
        """
        try:
            query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'reporting_data'"
            tables = self.execute_query(query)  # Use self.execute_query to call the local method
            if tables:
                self.logger.info("Fetched all table names successfully.")
            return tables
        except Exception as e:
            self.logger.error(f"Error fetching table names: {str(e)}")
            return []

    def get_newest_crawl_date(self):
        """
        Fetch the newest crawl date from the 'rpt_job_openings_metrics' table in the 'reporting_data' schema.
        """
        try:
            # Prepare the SQL query to fetch the maximum crawl date
            query = "SELECT MAX(crawl_date) AS newest_crawl_date FROM reporting_data.rpt_job_openings_metrics"
            
            # Execute the query and fetch the result
            crawl_date_result = self.execute_query(query)  # Use self.execute_query to call the local method
            
            # Check if any result is returned
            if crawl_date_result and crawl_date_result[0][0] is not None:
                newest_crawl_date = crawl_date_result[0][0]  # Assume it's already a string
                self.logger.info(f"Fetched the newest crawl date successfully: {newest_crawl_date}")
                return newest_crawl_date
            else:
                self.logger.info("No crawl dates found.")
                return None
        except Exception as e:
            self.logger.error(f"Error fetching the newest crawl date: {str(e)}")
            return None

    def fetch_openings_statistics_metrics(self, crawl_date):
        """
        Fetch data for openings statistics metrics within the 'reporting_data' schema using a given crawl date.
        """
        try:
            # Prepare the SQL query to fetch the required data
            query = f"""
                SELECT 
                    AAAA.total_openings
                    , COALESCE(((AAAA.total_openings - AAAA.prev_total_openings) / NULLIF(CAST(AAAA.prev_total_openings AS FLOAT), 0)) * 100.0, 0) AS total_openings_change_pct
                    , AAAA.closed_openings_count
                    , COALESCE(((AAAA.closed_openings_count - AAAA.prev_closed_openings_count) / NULLIF(CAST(AAAA.prev_closed_openings_count AS FLOAT), 0)) * 100.0, 0) AS closed_openings_change_pct
                    , AAAA.new_openings_count
                    , COALESCE(((AAAA.new_openings_count - AAAA.prev_new_openings_count) / NULLIF(CAST(AAAA.prev_new_openings_count AS FLOAT), 0)) * 100.0, 0) AS new_openings_change_pct
                    , AAAA.fill_rate
                    , COALESCE(((AAAA.fill_rate - AAAA.prev_fill_rate) / NULLIF(CAST(AAAA.prev_fill_rate AS FLOAT), 0)) * 100.0, 0) AS fill_rate_change_pct
                    , AAAA.average_weeks_to_fill
                    , COALESCE(((AAAA.average_weeks_to_fill - AAAA.prev_average_weeks_to_fill) / NULLIF(CAST(AAAA.prev_average_weeks_to_fill AS FLOAT), 0)) * 100.0, 0) AS average_weeks_to_fill_change_pct
                    , AAAA.crawl_date
                FROM(
                    SELECT 
                        AAA.total_openings
                        , LEAD(AAA.total_openings) OVER (ORDER BY AAA.crawl_date DESC) AS prev_total_openings
                        , AAA.closed_openings_count
                        , LEAD(AAA.closed_openings_count) OVER (ORDER BY AAA.crawl_date DESC) AS prev_closed_openings_count
                        , AAA.new_openings_count
                        , LEAD(AAA.new_openings_count) OVER (ORDER BY AAA.crawl_date DESC) AS prev_new_openings_count
                        , AAA.fill_rate
                        , LEAD(AAA.fill_rate) OVER (ORDER BY AAA.crawl_date DESC) AS prev_fill_rate
                        , BBB.average_weeks_to_fill 
                        , LEAD(BBB.average_weeks_to_fill) OVER (ORDER BY AAA.crawl_date DESC) AS prev_average_weeks_to_fill 
                        , AAA.crawl_date
                    FROM reporting_data.rpt_job_openings_metrics AAA
                    LEFT JOIN (
                        SELECT BBB.*
                        FROM reporting_data.rpt_job_fill_time_statistics BBB
                        WHERE BBB.current_date BETWEEN TO_CHAR(CAST('{crawl_date}' AS date) - INTERVAL '7 days', 'YYYY-MM-DD') AND '{crawl_date}'   
                    ) BBB ON AAA.crawl_date = BBB.current_date
                    WHERE AAA.crawl_date BETWEEN TO_CHAR(CAST('{crawl_date}' AS date) - INTERVAL '7 days', 'YYYY-MM-DD') AND '{crawl_date}'
                    ORDER BY AAA.crawl_date DESC
                )AAAA
                WHERE AAAA.crawl_date = '{crawl_date}'
            """
            # Execute the query and fetch the result
            data = self.execute_query(query)  # Use self.execute_query to call the local method
            
            # Convert the data into a DataFrame if not empty
            if data:
                df = pd.DataFrame(data, columns=['total_openings', 'total_openings_change_pct', 'closed_openings_count', 'closed_openings_change_pct', 'new_openings_count', 'new_openings_change_pct', 'fill_rate', 'fill_rate_change_pct', 'average_weeks_to_fill', 'average_weeks_to_fill_change_pct', 'crawl_date'])
                self.logger.info("Data converted to DataFrame successfully.")
                return df
            else:
                self.logger.info("No data found for the given crawl date.")
                return pd.DataFrame()  # Return an empty DataFrame if no data
        except Exception as e:
            self.logger.error(f"Error fetching openings statistics metrics for crawl date {crawl_date}: {str(e)}")
            return pd.DataFrame()  # Return an empty DataFrame in case of an error

    def fetch_openings_history(self):
        """
        Fetch data for history total openings statistics metrics within the 'reporting_data' schema.
        """
        try:
            # Prepare the SQL query to fetch the required data
            query = """
                SELECT 
                    AAA.total_openings
                    , AAA.crawl_date
                FROM(
                    SELECT AA.total_openings, AA.crawl_date 
                    FROM reporting_data.rpt_job_openings_metrics AA 
                    ORDER BY AA.crawl_date 
                    LIMIT 12
                )AAA
                ORDER BY AAA.crawl_date ASC 
            """
            # Execute the query and fetch the result
            data = self.execute_query(query)  # Use self.execute_query to call the local method

            # Convert the data into a DataFrame if not empty
            if data:
                df = pd.DataFrame(data, columns=['total_openings', 'crawl_date'])
                self.logger.info("Historical total openings data converted to DataFrame successfully.")
                return df
            else:
                self.logger.info("No historical total openingsdata found for openings statistics.")
                return pd.DataFrame()  # Return an empty DataFrame if no data
        except Exception as e:
            self.logger.error("Error fetching historical openings statistics metrics: {error}".format(error=str(e)))
            return pd.DataFrame()  # Return an empty DataFrame in case of an error
