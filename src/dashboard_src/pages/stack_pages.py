## import packages
# import necessary libraries
import sys, os 
import json
from datetime import datetime, timedelta
import pandas as pd
# import geopandas as gpd
import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

# set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_root)

# import modules
from utils.log_utils import set_logger
from utils.dashboard_utils import FetchReportData, CreateReportChart

## Load data
# define fetch functions
    
# Integrate the fetch functions into the load_stack_page_data function
def load_stack_page_data():
    """
    Load reporting data from the database for the dashboard stack page.
    """
    # Setup logger
    logger = set_logger()

    # Initialize the FetchReportData class to handle database operations
    fetcher = FetchReportData(logger)

    # Fetch the data for different metrics from the stack page

    # load data for tool by data role
    tool_by_data_role = FetchReportData.fetch_tool_by_data_role(fetcher)

    # Close the database connection safely
    if fetcher.connection:
        fetcher.connection.close()
        logger.info("Database connection closed.")
    
    return tool_by_data_role

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
    tool_by_data_role = load_stack_page_data()

    # Check for missing category values and handle them
    tool_by_data_role['category'] = tool_by_data_role['category'].fillna('Others')

    # Create dropdown options
    data_roles = [{'label': role, 'value': role} for role in tool_by_data_role['data_role'].unique()]
    data_roles.insert(0, {'label': 'All', 'value': 'All'})

    categories = [{'label': category, 'value': category} for category in tool_by_data_role['category'].unique()]
    categories.insert(0, {'label': 'All', 'value': 'All'})

    # Create figture
    tool_popularity_bar_chart = CreateReportChart.create_tool_popularity_bar_chart(tool_by_data_role)

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
                                                html.Div(
                                                    className="group-dropdown-item",
                                                    children=[
                                                        html.Label("Select Technology Group", className="group-label"),
                                                        dcc.Dropdown(
                                                            id='category-dropdown',
                                                            options=categories,
                                                            value='All'
                                                        ),
                                                    ]
                                                ),
                                                html.Div(
                                                    className="role-dropdown-item",
                                                    children=[
                                                        html.Label("Select Data Role", className="role-label"),
                                                        dcc.Dropdown(
                                                            id='datarole-dropdown',
                                                            options=data_roles,
                                                            value='All'
                                                        ),
                                                    ]
                                                ),
                                                html.P("Tool Trends", className="tool-trend-title"),
                                                html.P("Tracking the trends of the most maintion tools in data-centric jobs", className="tool-trend-sub-title"),
                                                dcc.Graph(id='line-chart', className="tool-trends-line-chart"),
                                                html.P("Top 5 Stacks with Most Openings", className="tool-broad-title"),
                                                html.P("Top 5 most maintioned technologies of all time", className="tool-broad-sub-title"),
                                                html.P("Most popular in", className="most-popular-title"),
                                                html.P("Least popular in", className="least-popular-title"),
                                                dcc.Graph(figure=tool_popularity_bar_chart, className="tool-popularity-bar-chart"),
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

# Define callback function
@callback(
    Output('line-chart', 'figure'),
    [Input('datarole-dropdown', 'value'),
     Input('category-dropdown', 'value')]
)
def update_charts(selected_datarole, selected_category):
    tool_by_data_role = load_stack_page_data()
    line_chart = CreateReportChart.create_tool_trends_line_chart(tool_by_data_role, selected_datarole, selected_category)
    return line_chart