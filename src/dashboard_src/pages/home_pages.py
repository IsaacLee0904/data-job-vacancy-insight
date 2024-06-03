## import packages
# import necessary libraries
import sys, os 
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from flask import Flask, send_from_directory

# set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_root)

# import modules
from utils.log_utils import set_logger
from utils.front_end_utils import load_css_files
from utils.dashboard_utils import FetchReportData

## Load data
# define fetch functions
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

def fetch_openings_company_for_dashboard(fetcher, crawl_date):
    """
    Fetch job vacancy data from the database for a given crawl date and verify if the data matches the crawl date.
    """
    data = fetcher.fetch_openings_company(crawl_date)
    if not data.empty:
        # Ensure date formats are consistent for comparison
        data['crawl_date'] = pd.to_datetime(data['crawl_date']).dt.date
        provided_date = pd.to_datetime(crawl_date).date()

        # Verify that all records have the correct crawl date
        if all(data['crawl_date'] == provided_date):
            fetcher.logger.info("Job vacancy information successfully validated for the provided crawl date.")
            return data
        else:
            fetcher.logger.error("Data inconsistency detected: 'crawl_date' does not match the provided date in job vacancy data.")
            # Optionally, return only consistent data or handle inconsistency here
            consistent_data = data[data['crawl_date'] == provided_date]
            return consistent_data if not consistent_data.empty else pd.DataFrame()
    else:
        fetcher.logger.info(f"No job vacancy data available for the crawl date: {crawl_date}.")
        return pd.DataFrame()

def fetch_taiepi_area_openings_for_dashboard(fetcher, crawl_date):
    """
    Fetch job vacancy data for the Taipei and New Taipei area from the database for a given crawl date and verify if the data matches the crawl date.
    """
    data = fetcher.fetch_taiepi_area_openings(crawl_date)
    if not data.empty:
        # Ensure date formats are consistent for comparison
        data['crawl_date'] = pd.to_datetime(data['crawl_date']).dt.date
        provided_date = pd.to_datetime(crawl_date).date()

        # Verify that all records have the correct crawl date
        if all(data['crawl_date'] == provided_date):
            fetcher.logger.info("Job vacancy information for the Taipei area successfully validated for the provided crawl date.")
            return data
        else:
            fetcher.logger.error("Data inconsistency detected: 'crawl_date' does not match the provided date in job vacancy data for the Taipei area.")
            # Optionally, return only consistent data or handle inconsistency here
            consistent_data = data[data['crawl_date'] == provided_date]
            return consistent_data if not consistent_data.empty else pd.DataFrame()
    else:
        fetcher.logger.info(f"No job vacancy data available for the Taipei area on the crawl date: {crawl_date}.")
        return pd.DataFrame()

# Integrate the fetch functions into the load_home_page_data function
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
        # load data for historical total openings line chart
        historical_total_openings = fetch_historical_total_openings_for_dashboard(fetcher)
        # load data for data role pie plot
        data_role = fetch_data_role_for_dashboard(fetcher, newest_crawl_date)
        # load data for data tools top 3 
        data_tools = fetch_data_tools_for_dashboard(fetcher, newest_crawl_date)
        # load data for openings company top 5
        openings_company = fetch_openings_company_for_dashboard(fetcher, newest_crawl_date)
        # load data fro taiepi area openings
        taiepi_area_openings = fetch_taiepi_area_openings_for_dashboard(fetcher, newest_crawl_date)
        
    else:
        logger.info("No newest crawl date available.")

    # Close the database connection safely
    if fetcher.connection:
        fetcher.connection.close()
        logger.info("Database connection closed.")
    
    return openings_statistics, historical_total_openings, data_role, data_tools, openings_company, taiepi_area_openings

layout = html.Div(
    className="frame",
    children=[
        html.Div(
            className="div",
            children=[
                html.Div(
                    className="group",
                    children=[
                        html.Div("MidnightGuy", className="text-wrapper"),
                        html.Div(
                            className="overlap-group-wrapper",
                            children=[
                                html.Div(
                                    className="overlap-group",
                                    children=[
                                        html.Div(className="ellipse"),
                                        html.Div(className="ellipse-2"),
                                    ],
                                )
                            ],
                        ),
                    ],
                ),
                # author
                html.Div(
                    className="group-2",
                    children=[
                        html.Div("Isaac Lee", className="text-wrapper-2"),
                        html.Div("Data Engineer", className="text-wrapper-3"),
                    ],
                ),
                # navigation menu
                html.Div(
                    className="group-3",
                    children=[
                        html.Div(
                            className="group-4",
                            children=[
                                html.A("Home", href="/", className="text-wrapper-4"),
                                html.Img(src="assets/icons/home.svg", className="img"),
                            ],
                        ),
                        html.Div(className="rectangle"),
                    ],
                ),
                html.Div(className="rectangle-2"),
                html.Div(
                    className="component",
                    children=[
                        html.Div(
                            className="div-wrapper",
                            children=[
                                html.A("Geography", href="/geography", className="text-wrapper-5"),
                            ],
                        ),
                        html.Img(src="assets/icons/geography.svg", className="img"),
                    ],
                ),
                html.Div(
                    className="component-2",
                    children=[
                        html.Div(
                            className="group-5",
                            children=[
                                html.A("Education", href="/education", className="text-wrapper-6"),
                            ],
                        ),
                        html.Img(src="assets/icons/education.svg", className="img-2"),
                    ],
                ),
                html.Div(
                    className="component-3",
                    children=[
                        html.Div(
                            className="group-6",
                            children=[
                                html.A("Stack", href="/stack", className="text-wrapper-7"),
                            ],
                        ),
                        html.Img(src="assets/icons/stack.svg", className="img-2"),
                    ],
                ),
                html.Div(
                    className="overlap",
                    children=[
                        html.Div(
                            className="chart",
                            children=[
                                # html.Img(src="assets/img/profile.png", className="s"),
                                html.Img(src="assets/img/ellipse-17.svg", className="ellipse-3"),
                            ],
                        ),
                    ],
                ),
                html.Img(src="assets/img/ellipse-18.png", className="ellipse-4"),
            ],
        ),
    ],
),
    
    # Main Content
#     html.Div([
#         html.H1("Dashboard", className="main-title"),
#         html.Div([
#             html.Div([
#                 html.H3("Total Openings"),
#                 html.P("vs last week"),
#             ], className="metric"),
#             html.Div([
#                 html.H3("New Openings"),
#                 html.P("vs last week"),
#             ], className="metric"),
#             html.Div([
#                 html.H3("Fill Rate"),
#                 html.P("vs last week"),
#             ], className="metric"),
#             html.Div([
#                 html.H3("ATTF"),
#                 html.P("vs last week"),
#             ], className="metric"),
#         ], className="metrics-row"),
#         html.Div([
#             html.H3("Openings Metrics in the Last 3 Month"),
#             # Placeholder for graph
#             html.Div(id="openings-metrics-graph", className="graph-placeholder"),
#         ], className="section"),
#         html.Div([
#             html.Div([
#                 html.H3("Stacks of the week"),
#                 # Placeholder for bubble chart
#                 html.Div(id="stacks-of-week-chart", className="bubble-chart-placeholder"),
#             ], className="chart-section"),
#             html.Div([
#                 html.H3("Top 5 Companies with Most Openings"),
#                 html.Table([
#                     html.Tr([html.Th("#"), html.Th("Company"), html.Th("Openings")]),
#                     html.Tr([html.Td("01"), html.Td("Company A"), html.Td("100")]),
#                     html.Tr([html.Td("02"), html.Td("Company B"), html.Td("90")]),
#                     html.Tr([html.Td("03"), html.Td("Company C"), html.Td("80")]),
#                     html.Tr([html.Td("04"), html.Td("Company D"), html.Td("70")]),
#                     html.Tr([html.Td("05"), html.Td("Company E"), html.Td("60")]),
#                 ], className="openings-table"),
#             ], className="table-section"),
#             html.Div([
#                 html.H3("Openings in Taipei"),
#                 # Placeholder for map/chart
#                 html.Div(id="openings-in-taipei-chart", className="map-placeholder"),
#             ], className="chart-section"),
#         ], className="bottom-section"),
#     ], className="main-content"),
# ], className="container")

# Run the server
if __name__ == '__main__':
    openings_statistics, historical_total_openings, data_role, data_tools, openings_company, taiepi_area_openings = load_home_page_data()