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
        # load data for openings statistics metrics
        openings_statistics = fetch_openings_statistics_for_dashboard(fetcher, newest_crawl_date)
        print(openings_statistics.head())
        # load data for historical total openings line chart
        historical_total_openings = fetch_historical_total_openings_for_dashboard(fetcher)
        print(historical_total_openings.head())
        # load data for data role pie plot
        data_role = fetch_data_role_for_dashboard(fetcher, newest_crawl_date)
        print(data_role.head())
        # load data for data tools top 3 
        data_tools = fetch_data_tools_for_dashboard(fetcher, newest_crawl_date)
        print(data_tools.head())
        
    else:
        logger.info("No newest crawl date available.")

    # Close the database connection safely
    if fetcher.connection:
        fetcher.connection.close()
        logger.info("Database connection closed.")

def fetch_openings_statistics_for_dashboard(fetcher, crawl_date):
    """
    Fetch openings statistics metrics from the database for a given crawl date and verify if the data matches the crawl date.
    """
    data = fetcher.fetch_openings_statistics_metrics(crawl_date)
    if not data.empty:
        # Verify that all records have the correct crawl date
        if all(data['crawl_date'] == crawl_date):
            return data
        else:
            fetcher.logger.error("Data inconsistency detected: 'crawl_date' does not match the provided date.")
            # Return only consistent data or handle inconsistency here
            return pd.DataFrame()
    else:
        fetcher.logger.info("No data available for openings statistics on the provided crawl date.")
        return pd.DataFrame()

def fetch_historical_total_openings_for_dashboard(fetcher):
    """
    Fetch historical total openings data and ensure it includes the newest crawl date.
    """
    data = fetcher.fetch_openings_history()
    if not data.empty:
        newest_crawl_date = fetcher.get_newest_crawl_date()
        max_crawl_date = data['crawl_date'].max()
        if pd.to_datetime(max_crawl_date) == pd.to_datetime(newest_crawl_date):
            return data
        else:
            fetcher.logger.error(f"Data inconsistency detected: The newest data in historical openings (date: {max_crawl_date}) does not match the newest crawl date ({newest_crawl_date}).")
            return pd.DataFrame()  # Return empty DataFrame in case of inconsistency
    else:
        fetcher.logger.info("No historical data available for total openings.")
        return pd.DataFrame()

def fetch_data_role_for_dashboard(fetcher, crawl_date):
    """
    Fetch data role data from the database for a given crawl date and verify if the data matches the crawl date.
    """
    data = fetcher.fetch_data_role(crawl_date)
    if not data.empty:
        # Ensure date formats are consistent for comparison
        data['crawl_date'] = pd.to_datetime(data['crawl_date']).dt.date
        provided_date = pd.to_datetime(crawl_date).date()

        # Verify that all records have the correct crawl date
        if all(data['crawl_date'] == provided_date):
            return data
        else:
            fetcher.logger.error("Data inconsistency detected: 'crawl_date' does not match the provided date.")
            # Return only consistent data or handle inconsistency here
            return pd.DataFrame()
    else:
        fetcher.logger.info("No data available for data roles on the provided crawl date.")
        return pd.DataFrame()

def fetch_data_tools_for_dashboard(fetcher, crawl_date):
    """
    Fetch data tools data from the database for a given crawl date and verify if the data matches the crawl date.
    """
    data = fetcher.fetch_data_tool(crawl_date)
    if not data.empty:
        # Ensure date formats are consistent for comparison
        data['crawl_date'] = pd.to_datetime(data['crawl_date']).dt.date
        provided_date = pd.to_datetime(crawl_date).date()

        # Verify that all records have the correct crawl date
        if all(data['crawl_date'] == provided_date):
            fetcher.logger.info("Data tools information successfully validated for the provided crawl date.")
            return data
        else:
            fetcher.logger.error("Data inconsistency detected: 'crawl_date' does not match the provided date in data tools information.")
            # Optionally, return only consistent data or handle inconsistency here
            consistent_data = data[data['crawl_date'] == provided_date]
            return consistent_data if not consistent_data.empty else pd.DataFrame()
    else:
        fetcher.logger.info(f"No data tools information available for the crawl date: {crawl_date}.")
        return pd.DataFrame()

# Run the server
if __name__ == '__main__':
    load_home_page_data()
    # app.run_server(debug=True, host='0.0.0.0', port=9100)