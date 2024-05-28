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

app.layout = html.Div([
    html.Div(className="sidebar", children=[
        html.H2("Dashboard"),
        html.A("Home", href="/", className="nav-link"),
        # html.A("Stack", href="/stack", className="nav-link"),
        # html.A("Education", href="/education", className="nav-link"),
        # html.A("Geography", href="/geography", className="nav-link"),
    ]),
    html.Div(className="content", children=[
        dcc.Location(id="url"),
        html.Div(id="page-content")
    ])
])

# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/stack':
#         return stack_page_layout()
#     elif pathname == '/education':
#         return education_page_layout()
#     elif pathname == '/geography':
#         return geography_page_layout()
#     else:
#         return home_page_layout()

# def stack_page_layout():
#     return html.Div([
#         html.H2('Stack Page')
#         # 其他內容
#     ])

# def education_page_layout():
#     return html.Div([
#         html.H2('Education Page')
#         # 其他內容
#     ])

# def geography_page_layout():
#     return html.Div([
#         html.H2('Geography Page')
#         # 其他內容
#     ])

# def home_page_layout():
#     return html.Div([
#         html.H2('Home Page'),
#         html.Iframe(src='/assets/front_end/html/page.html', style={'width': '100%', 'height': '600px'})
#     ])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=9100)