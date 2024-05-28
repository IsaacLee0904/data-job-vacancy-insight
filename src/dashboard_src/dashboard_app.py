import sys, os 
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

css_directory = os.path.join(project_root, 'assets', 'front_end', 'css')
external_stylesheets = load_css_files(css_directory)

server = Flask(__name__)

def create_dash_application(flask_app):
    app = dash.Dash(
        __name__,
        server=flask_app,  
        external_stylesheets=external_stylesheets,
        meta_tags=[
            {
                "name": "viewport",
                "content": "width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no",
            }
        ]
    )
    app.title = "Data Job Market Insight Dashboard"
    app.config.suppress_callback_exceptions = True

    app.layout = html.Div([
    html.Div(className="frame-1364", children=[
        html.Div(className="container-2", children=[
            html.Div(className="group-2", children=[
                html.Img(className="group-1", src="/assets/front_end/assets/vectors/group_11_x2.svg"),
                html.Span("MidnightGuy", className="midnight-guy")
            ]),
            html.Img(className="chart-5", src="/assets/front_end/assets/vectors/chart_5_x2.svg"),
            html.Div(className="group-54", children=[
                html.Div("Isaac Lee", className="isaac-lee"),
                html.Span("Data Engineer", className="data-engineer")
            ]),
            html.Div(className="group-56", children=[
                html.Div(className="rectangle-7"),
                html.Div(className="group-52", children=[
                    html.Div(className="dashboard-black-24-dp-11", children=[
                        html.Img(className="vector", src="/assets/front_end/assets/vectors/vector_9_x2.svg")
                    ]),
                    html.Span("Home", className="home")
                ])
            ]),
            html.Div(className="component-1", children=[
                html.Div(className="code-slash", children=[
                    html.Img(className="vector-1", src="/assets/front_end/assets/vectors/vector_1_x2.svg")
                ]),
                html.Div(className="group-51", children=[
                    html.Span("Stack", className="stack")
                ])
            ]),
            html.Div(className="container-1", children=[
                html.Div(className="component-2", children=[
                    html.Div(className="book-02", children=[
                        html.Img(className="icon-1", src="/assets/front_end/assets/vectors/icon_1_x2.svg")
                    ]),
                    html.Div(className="group-50", children=[
                        html.Span("Education", className="education")
                    ])
                ]),
                html.Div(className="rectangle-11")
            ]),
            html.Div(className="component-3", children=[
                html.Div(className="map-03", children=[
                    html.Img(className="icon", src="/assets/front_end/assets/vectors/icon_3_x2.svg")
                ]),
                html.Div(className="group-49", children=[
                    html.Span("Geography", className="geography")
                ])
            ])
        ]),
        html.Div(className="container", children=[
            html.Div(className="s-2308096061")
        ])
    ]),
    html.Div(className="content", children=[
        dcc.Location(id="url"),
        html.Div(id="page-content")
    ])
])

    return app

# set front end assets path
@server.route('/assets/front_end/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(os.path.join(project_root, 'assets', 'front_end'), filename)

# Load data

app = create_dash_application(server)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=9100)