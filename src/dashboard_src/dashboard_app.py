import sys, os 
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from flask import Flask, send_from_directory

# set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utils.log_utils import set_logger
from utils.front_end_utils import load_css_files
from utils.dashboard_utils import FetchReportData

css_directory = os.path.join(project_root, 'assets', 'front_end', 'css')
external_stylesheets = load_css_files(css_directory)

# Load data
def load_home_page_data():
    """
    Load reporting data from the database for the dashboard home page.
    """
    # Setup logger
    logger = set_logger()

    # Initialize the FetchReportData class to handle database operations
    fetcher = FetchReportData(logger)

    # Get the newest crawl date
    newest_crawl_date = fetcher.get_newest_crawl_date()

    # Fetch the data for different metrics from the home page
    if newest_crawl_date:
        logger.info(f"Fetching data for the date: {newest_crawl_date}")
        openings_statistics = fetch_openings_statistics(fetcher, newest_crawl_date)
        historical_total_openings = fetch_historical_total_openings(fetcher)
        
        # Check if data is available
        if not openings_statistics.empty:
            # Verify that the 'crawl_date' column matches the 'newest_crawl_date'
            if all(openings_statistics['crawl_date'] == newest_crawl_date):
                print("All records match the newest crawl date.")
                # print(openings_statistics.head()
                print(historical_total_openings.head())
            else:
                logger.error("Data inconsistency detected: 'crawl_date' does not match 'newest_crawl_date'.")
                # Optionally, handle the inconsistency by filtering or other means
                consistent_data = openings_statistics[openings_statistics['crawl_date'] == newest_crawl_date]
                if not consistent_data.empty:
                    print(consistent_data.head())
                else:
                    logger.info("No consistent data available after filtering.")
    else:
        logger.info("No data available for openings statistics.")

    # Close the database connection safely
    if fetcher.connection:
        fetcher.connection.close()
        logger.info("Database connection closed.")

def fetch_openings_statistics(fetcher, crawl_date):
    """
    Fetch openings statistics metrics from the database.
    """
    return fetcher.fetch_openings_statistics_metrics(crawl_date)

def fetch_historical_total_openings(fetcher):
    """
    Fetch openings statistics metrics from the database.
    """
    return fetcher.fetch_openings_history()

# Additional fetch functions can be defined here as needed
# def fetch_another_metrics(fetcher, crawl_date):
#     ...

# Run the server
if __name__ == '__main__':
    load_home_page_data()
    # app.run_server(debug=True, host='0.0.0.0', port=9100)