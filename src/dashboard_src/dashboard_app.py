import sys, os 
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# setup project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utils.log_utils import set_logger
from utils.front_end_utils import load_css_files

css_directory = 'assets/front_end/css'
external_stylesheets = load_css_files(css_directory)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# app.layout = html.Div([
#     html.Div(className="sidebar", children=[
#         html.H2("Dashboard"),
#         html.A("Home", href="/", className="nav-link"),
#         html.A("Stack", href="/stack", className="nav-link"),
#         html.A("Education", href="/education", className="nav-link"),
#         html.A("Geography", href="/geography", className="nav-link"),
#     ]),
#     html.Div(className="content", children=[
#         html.H2("Welcome to the Dashboard"),
#         dcc.Location(id="url"),
#         html.Div(id="page-content")
#     ])
# ])