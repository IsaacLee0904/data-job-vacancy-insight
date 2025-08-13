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
def load_edu_page_data_from_database():
    """
    Load reporting data from the database for the dashboard edu page (fallback).
    """
    # Setup logger
    logger = set_logger()

    # Initialize the FetchReportData class to handle database operations
    fetcher = FetchReportData(logger)

    # Get the newest crawl date
    newest_crawl_date = fetcher.get_newest_crawl_date()
    logger.info(f'Database fallback - newest crawl date: {newest_crawl_date}')

    # load data for tool by data role
    edu_by_data_role = FetchReportData.fetch_education_by_data_role(fetcher, newest_crawl_date)

    # Close the database connection safely
    if fetcher.connection:
        fetcher.connection.close()
        logger.info("Database connection closed.")
    
    return edu_by_data_role

def load_edu_page_data():
    """
    Load education page data with API fallback to database
    """
    logger = set_logger()
    
    if USE_API:
        logger.info("Attempting to load education page data via API...")
        try:
            # Initialize API data service
            data_service = DashboardDataService(api_base_url="http://localhost:8000", logger=logger)
            
            # Check API connection
            if not data_service.check_api_connection():
                logger.warning("API not available, falling back to database")
                return load_edu_page_data_from_database()
            
            # Use education-specific API endpoint
            education_data = data_service.api_client.get_education_by_data_role()
            if education_data:
                logger.info("Successfully loaded education data via API")
                import pandas as pd
                edu_by_data_role = pd.DataFrame(education_data)
                return edu_by_data_role
            else:
                logger.warning("No education data available from API, falling back to database")
                return load_edu_page_data_from_database()
            
        except Exception as e:
            logger.error(f"Error loading data via API: {e}")
            logger.info("Falling back to database")
            return load_edu_page_data_from_database()
    else:
        logger.info("Using database directly")
        return load_edu_page_data_from_database()

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
    edu_by_data_role = load_edu_page_data()

    edu_heatmap = CreateReportChart.create_education_heatmap(edu_by_data_role)

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
                                                html.P("Educational Requirements for Data Roles", className="edu-title"),
                                                html.P("A Comprehensive Overview of the Academic Backgrounds Sought in Data-Centric Careers", className="edu-sub-title"),
                                                dcc.Graph(figure=edu_heatmap, className="edu-heatmap"),
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