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
from src.core.log_utils import set_logger
from src.core.front_end_utils import load_css_files
from src.core.dashboard_utils import FetchReportData, CreateReportChart
from src.dashboard.api_client import DashboardDataService

## Configuration
USE_API = True  # Set to False to use database directly

## Load data
def load_geo_page_data_from_database():
    """
    Load reporting data from the database for the dashboard geo page (fallback).
    """
    # Setup logger
    logger = set_logger()

    # Initialize the FetchReportData class to handle database operations
    fetcher = FetchReportData(logger)

    # Get the newest crawl date
    newest_crawl_date = fetcher.get_newest_crawl_date()
    logger.info(f'Database fallback - newest crawl date: {newest_crawl_date}')

    # load data for geography analysis
    taiwan_openings = FetchReportData.fetch_taiwan_openings(fetcher, newest_crawl_date)
    six_major_city_openings = FetchReportData.fetch_major_city_openings(fetcher, newest_crawl_date)
    taipei_openings_trend = FetchReportData.fetch_taipei_historical_openings(fetcher)

    # Close the database connection safely
    if fetcher.connection:
        fetcher.connection.close()
        logger.info("Database connection closed.")
    
    return taiwan_openings, six_major_city_openings, taipei_openings_trend

def load_geo_page_data():
    """
    Load geography page data with API fallback to database
    """
    logger = set_logger()
    
    if USE_API:
        logger.info("Attempting to load geography page data via API...")
        try:
            # Initialize API data service
            data_service = DashboardDataService(api_base_url="http://localhost:8000", logger=logger)
            
            # Check API connection
            if not data_service.check_api_connection():
                logger.warning("API not available, falling back to database")
                return load_geo_page_data_from_database()
            
            # Use geography-specific API endpoints
            taiwan_data = data_service.api_client.get_taiwan_openings()
            cities_data = data_service.api_client.get_major_city_openings()
            taipei_historical_data = data_service.api_client.get_taipei_historical_openings()
            
            if taiwan_data is not None and cities_data is not None and taipei_historical_data is not None:
                logger.info("Successfully loaded geography data via API")
                import pandas as pd
                taiwan_openings = pd.DataFrame(taiwan_data)
                six_major_city_openings = pd.DataFrame(cities_data)
                taipei_openings_trend = pd.DataFrame(taipei_historical_data)
                return taiwan_openings, six_major_city_openings, taipei_openings_trend
            else:
                logger.warning("Some geography data not available from API, falling back to database")
                return load_geo_page_data_from_database()
            
        except Exception as e:
            logger.error(f"Error loading data via API: {e}")
            logger.info("Falling back to database")
            return load_geo_page_data_from_database()
    else:
        logger.info("Using database directly")
        return load_geo_page_data_from_database()

def sidebar():
    return html.Div(
        className="sidebar",
        children=[
            html.Div(
                className="profile",
                children=[
                    html.Div("DataWonderlust", className="watermark"),
                    html.Div(
                        className="watermark-icon",
                        children=[
                            html.Div(
                                className="watermark-icon-group",
                                children=[
                                    html.Div(className="watermark-icon-1"),
                                    html.Div(className="watermark-icon-2")
                                ]
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                className="creator-info",
                children=[
                    html.Div("Isaac Lee", className="creator-name"),
                    html.Div("Data Engineer", className="creator-title")
                ]
            ),
            html.Div(
                className="home-component",
                children=[
                    html.Div(
                        className="selection-home",
                        children=[
                            html.A("Home", href="/", className="homepage-text"),
                            html.Img(src="assets/icons/home.svg", className="selection-icon")
                        ]
                    ),                
                ]
            ),
            html.Div(
                className="stack-component",
                children=[
                    html.Div(
                        className="selection-stack",
                        children=[html.A("Stack", href="/stack", className="stack-text")]
                    ),
                    html.Img(src="assets/icons/stack.svg", className="selection-icon"),
                ]
            ),
            html.Div(
                className="geography-component",
                children=[
                    html.Div(
                        className="selection-geography",
                        children=[html.A("Geography", href="/geography", className="geography-text")]
                    ),
                    html.Img(src="assets/icons/geography.svg", className="selection-icon")
                ]
            ),
            html.Div(
                className="education-component",
                children=[
                    html.Div(
                        className="selection-education",
                        children=[html.A("Education", href="/education", className="education-text")]
                    ),
                    html.Img(src="assets/icons/education.svg", className="selection-icon")
                ]
            ),
            html.Div(
                className="connection-info",
                children=[
                    html.Div(
                        className="connection-info-group",
                        children=[
                            html.Div(className="connection-info-shape"),
                            html.Div(
                                className="connection-info-title",
                                children=[html.Div("About Author :", className="connection-info-title-text")]
                            ),
                            html.Div(
                                className="github",
                                children=[html.A("Github", href="https://github.com/IsaacLee0904", className="connection-info-content")]
                            ),
                            html.Div(
                                className="linkedin",
                                children=[html.A("Linkedin", href="https://www.linkedin.com/in/isaac-lee-459a15143/", className="connection-info-content")]
                            ),
                            html.Div(
                                className="email",
                                children=[html.A("Email", href="hool19965401@gmail.com", className="connection-info-content")]
                            ),
                            html.Img(src="assets/icons/github.svg", className="github-icon"),
                            html.Img(src="assets/icons/linkedin.svg", className="linkedin-icon"),
                            html.Img(src="assets/icons/email.svg", className="email-icon")
                        ]
                    )
                ]
            ),
            html.Div(
                className="project-source",
                children=[
                    html.Div(
                        className="project-source-group",
                        children=[html.A("project-source", href="https://github.com/IsaacLee0904/Data-Job-Vacancy-Insight", className="project-source-text")]
                    ),
                    html.Img(src="assets/icons/link.svg", className="link-icon")
                ]
            ),
            html.Div(
                className="profile-pic",
                children=[
                    html.Div(
                        className="profile-pic-shape",
                        children=[
                                html.Img(src="assets/img/profile.png", className="profile_img"),
                                html.Img(src="assets/img/sidebar_ellipse.svg", className="profile-ellipse-1")]
                    ),               
                ]
            ),
            html.Img(src="assets/img/sidebar_ellipse.png", className="profile-ellipse-2")
        ]
    )

def page_content():
    # Load data for the stack page
    taiwan_openings ,six_major_city_openings, taipei_openings_trend = load_geo_page_data()
    taiwan_openings_map = CreateReportChart.create_taiwan_openings_map(taiwan_openings)
    six_major_city_openings_table = CreateReportChart.create_county_openings_table(six_major_city_openings)  
    taipei_openings_trend_chart = CreateReportChart.create_taipei_openings_trend_chart(taipei_openings_trend) 

    return html.Div(
            className="page",
            children=[
                html.Div(
                    className="div",
                    children=[
                        html.Div(
                            className="overlap",
                            children=[                          
                                html.Div(
                                    className="overlap-6",
                                    children=[
                                        html.Div(
                                            className="dropdowns",
                                            children=[                                            
                                                html.P("Job Openings Across Taiwan Regions", className="tw-geo-title"),
                                                html.P("A Detailed Analysis of Job Availability in Different Counties and Cities", className="tw-geo-sub-title"),
                                                dcc.Graph(figure=taiwan_openings_map, className="geo-taiwan-map"),
                                                html.P("Job Opportunities in Taiwan's Six Major Cities", className="major-city-title"),
                                                html.P("A Close Examination of Job Availability in the Six Leading Cities", className="major-city-sub-title"),
                                                dcc.Graph(figure=six_major_city_openings_table, className="six-major-city-table"),
                                                html.P("Recent Job Vacancy Trends in Taipei", className="taipei-trend-title"),
                                                html.P("Examining the Changes in Job Openings Over the Last Three Months", className="taipei-trend-sub-title"),
                                                dcc.Graph(figure=taipei_openings_trend_chart, className="taipei_openings_trend_chart"),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        html.Div("Dashboard", className="title-page")
                    ]
                )
            ]
        )

layout = html.Div(
    children=[
        sidebar(),
        page_content()
    ]
)

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)