import dash
from dash import dcc, html, Input, Output, State, ctx, dash_table, Patch
import pandas as pd
from dash.dash_table.Format import Format, Scheme
import dash_bootstrap_components as dbc


def layout_main():
    layout = html.Div([
        html.Br(),
        html.Div([
            html.Img(src='assets/logo.png', style={'height': '100px', 'margin-left': 'auto', 'margin-right': 'auto'}),
        ], style={'text-align': 'center', 'margin-bottom': '10px'}),

        html.Div([
            html.Br(),
            dcc.Upload(
                id='upload-data',
                children=html.Div(['Drag or ', html.A('select an Excel Pump Curve File!')]),
                style={
                    'width': '500px', 'height': '60px', 'lineHeight': '60px',
                    'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                    'textAlign': 'center', 'margin': 'auto'
                },
                multiple=False
            ),
        ], style={'textAlign': 'center'}),

        dcc.Download(id="download-json"),
        html.Br(),
        html.Div([
            html.H5(id='file-name-output')
        ], style={'textAlign': 'center'}),
    ])

    return layout

