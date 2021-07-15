import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc

import skimage.io as sio
from skimage.transform import rescale, resize, downscale_local_mean

image = sio.imread("soccer_fieldv3.jpeg")
img = image[:, :, 1]
t2 = img[:, int(img.shape[1] / 2):]

image_rescaled = rescale(t2, 0.25, anti_aliasing=False)
image_resized = resize(image_rescaled, (92, 84), anti_aliasing=True)

liverpool_def = pd.read_csv('Coefficients_Liverpool_Defense.csv')
liverpool_off = pd.read_csv('Coefficients_Liverpool_Offense.csv')

x = np.arange(0,60)
y = np.arange(-45, 45)
yt = np.array([[i] for i in y])
z = x * yt

layout = go.Layout(
    scene=dict(
        xaxis=dict(
            nticks=6, range=[0,60], ),
        yaxis=dict(
            nticks=8, range=[-45, 45], ),
        zaxis=dict(
            nticks=12, range=[-120, 120], ), ),
    # margin=dict(
    #     t=0, # top margin: 30px, you want to leave around 30 pixels to
    #           # display the modebar above the graph.
    #     b=10, # bottom margin: 10px
    #     l=20, # left margin: 10px
    #     r=20, # right margin: 10px
    # ),
    margin=dict(
        t=0,  # top margin: 30px, you want to leave around 30 pixels to
        # display the modebar above the graph.
        b=10,  # bottom margin: 10px
        l=20,  # left margin: 10px
        r=10,  # right margin: 10px
    ),
    width=600)

layout2 = go.Layout(
    scene=dict(
        xaxis=dict(
            nticks=6, range=[0, 60], ),
        yaxis=dict(
            nticks=8, range=[-45, 45], ),
        zaxis=dict(
            nticks=12, range=[-120, 120], ), ),
    # margin=dict(
    #     t=90, # top margin: 30px, you want to leave around 30 pixels to
    #           # display the modebar above the graph.
    #     b=0, # bottom margin: 10px
    #     l=10, # left margin: 10px
    #     r=10 # right margin: 10px
    # ),
    margin=dict(
        t=90,  # top margin: 30px, you want to leave around 30 pixels to
        # display the modebar above the graph.
        b=10,  # bottom margin: 10px
        l=10,  # left margin: 10px
        r=10,  # right margin: 10px
    ),
    width=550,height=500)

camera = dict(
    eye=dict(x=1.75, y=1, z=0.4)
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
server = app.server


app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.Div([
            dcc.Loading(id="loading-1",
                        children=[dcc.Graph(id='3D-graph', figure={})]),
        ], className='four columns'),
        html.Div([
            dcc.Loading(id="loading-2",
                        children=[dcc.Graph(id='2D-graph', figure={})]),
        ], className='four columns'),
        html.Div([
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Label([html.Strong('Minutes: '),
                        # dcc.Input(id='a', type='number', step=0.1, value=0.5),
                        dcc.Slider(
                            id='minutes_def',
                            min=0,
                            max=90,
                            step=1,
                            value=5),
                        html.Div(id='slider-drag-output',
                                 style={'margin-top': -20, 'margin-left': 26, 'padding-right': '140px'})
                        ]),
            html.Br(),
            html.Br(),
            html.Label(
                dbc.Button(id='my_button', n_clicks=0, children="Submit", color="success"),
                style={'font-weight': 'bold'}),
            html.Br()
        ], className='four columns'),
    ], className='row'),
    html.Div([
        html.Div([
            dcc.Loading(id="loading-3",
                        children=[dcc.Graph(id='3D-graph2', figure={})]),
        ], className='four columns'),
        html.Div([
            dcc.Loading(id="loading-4",
                        children=[dcc.Graph(id='2D-graph2', figure={})]),
        ], className='four columns'),
        html.Div([
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Label([html.Strong('Minutes: '),
                        # dcc.Input(id='a', type='number', step=0.1, value=0.5),
                        dcc.Slider(
                            id='minutes_def2',
                            min=0,
                            max=90,
                            step=1,
                            value=5),
                        html.Div(id='slider-drag-output2',
                                 style={'margin-top': -20, 'margin-left': 26, 'padding-right': '140px'})
                        ]),
            html.Br(),
            html.Br(),
            html.Label(
                dbc.Button(id='my_button2', n_clicks=0, children="Submit", color="success"),
                style={'font-weight': 'bold'}),
            html.Br()
        ], className='four columns'),
    ], className='row'),

])

# app.layout = html.Div(
#     [
#         dbc.Row([
#             dbc.Col(html.Div([
#                 dcc.Loading(id="loading-1",
#                             children=[dcc.Graph(id='3D-graph', figure={})])])),
#             dbc.Col(html.Div([
#                 dcc.Loading(id="loading-2",
#                             children=[dcc.Graph(id='2D-graph', figure={})])])),
#             dbc.Col(html.Div([
#                 html.Br(),
#                 html.Br(),
#                 html.Br(),
#                 html.Br(),
#                 html.Label([html.Strong('minutes: '),
#                             # dcc.Input(id='a', type='number', step=0.1, value=0.5),
#                             dcc.Slider(
#                                 id='minutes_def',
#                                 min=0,
#                                 max=90,
#                                 step=1,
#                                 value=5),
#                             html.Div(id='slider-drag-output',
#                                      style={'margin-top': -20, 'margin-left': 26, 'padding-right': '140px'})
#                             ]),
#                 html.Br(),
#                 html.Br(),
#                 html.Label(
#                     dbc.Button(id='my_button', n_clicks=0, children="Submit", color="success"),
#                     style={'font-weight': 'bold'}),
#                 html.Br()
#             ]))
#         ], align="start", no_gutters=True)
#     ])


@app.callback(Output('slider-drag-output', 'children'),
              [Input('minutes_def', 'value')])
def display_value(value):
    return 'Timestep: {} minutes'.format(value)

@app.callback(Output('slider-drag-output2', 'children'),
              [Input('minutes_def2', 'value')])
def display_value(value):
    return 'Timestep: {} minutes'.format(value)

@app.callback(
    Output(component_id='3D-graph', component_property='figure'),
    Input(component_id='my_button', component_property='n_clicks'),
    [State(component_id='minutes_def', component_property='value')],
    prevent_initial_call=False
)
def update_3d(n_clicks, minutes_def):
    with np.errstate(divide='ignore', invalid='ignore'):
        fig = go.Figure(
            data=[go.Surface(z=z, x=x, y=y, colorscale='blues', surfacecolor=np.zeros(90 * 80).reshape(90, 80)),
                  go.Surface(x=x, y=y, z=np.zeros(7200).reshape(90, 80),
                             surfacecolor=image_resized, colorscale='BuGn_r')],
            layout=layout)

        row = liverpool_def.iloc[minutes_def]

        a = 1 / (np.sqrt((x + 0) ** 2 + (yt + 0) ** 2)) * row['a']
        b = 1 / (np.sqrt((x - 30) ** 2 + (yt + 0) ** 2)) * row['b']
        c = 1 / (np.sqrt((x - 60) ** 2 + (yt + 0) ** 2)) * row['c']
        d = 1 / (np.sqrt((x - 15) ** 2 + (yt - 40) ** 2)) * row['d']
        e = 1 / (np.sqrt((x - 45) ** 2 + (yt - 40) ** 2)) * row['e']
        f = 1 / (np.sqrt((x - 15) ** 2 + (yt + 40) ** 2)) * row['f']
        g = 1 / (np.sqrt((x - 45) ** 2 + (yt + 40) ** 2)) * row['g']

        A = a + b + c + d + e + f + g

        A[A > 100] = 100
        A[A < -100] = -100

        fig.data[0].z = A

        fig.update_layout(scene_aspectmode='manual',
                          scene_aspectratio=dict(x=1, y=1, z=1),
                          scene_camera=camera)

        fig.update_layout(title='Liverpool [F.C. Women] Defensive (3D Surface)', title_x = 0.08, title_y=0.925)

        #fig.update_layout(margin=dict(b=0, t=0))

        fig.update_traces(showscale=False)

        return fig


@app.callback(
    Output(component_id='2D-graph', component_property='figure'),
    Input(component_id='my_button', component_property='n_clicks'),
    [State(component_id='minutes_def', component_property='value')],
    prevent_initial_call=False
)
def update_2d(n_clicks, minutes_def):
    with np.errstate(divide='ignore', invalid='ignore'):
        fig2 = go.Figure(
            data=[
                go.Contour(z=z, showscale=True, connectgaps=True)],
            layout=layout2)

        row = liverpool_def.iloc[minutes_def]

        a = 1 / (np.sqrt((x + 0) ** 2 + (yt + 0) ** 2)) * row['a']
        b = 1 / (np.sqrt((x - 30) ** 2 + (yt + 0) ** 2)) * row['b']
        c = 1 / (np.sqrt((x - 60) ** 2 + (yt + 0) ** 2)) * row['c']
        d = 1 / (np.sqrt((x - 15) ** 2 + (yt - 40) ** 2)) * row['d']
        e = 1 / (np.sqrt((x - 45) ** 2 + (yt - 40) ** 2)) * row['e']
        f = 1 / (np.sqrt((x - 15) ** 2 + (yt + 40) ** 2)) * row['f']
        g = 1 / (np.sqrt((x - 45) ** 2 + (yt + 40) ** 2)) * row['g']

        A = a + b + c + d + e + f + g

        A[A > 100] = 100
        A[A < -100] = -100

        #fig2.update_layout(margin=dict(b=0, t=0))

        fig2.update_layout(title='Liverpool [F.C. Women] Defensive (2D Contour)')



        fig2.data[0].z = A

        return fig2


@app.callback(
    Output(component_id='3D-graph2', component_property='figure'),
    Input(component_id='my_button2', component_property='n_clicks'),
    [State(component_id='minutes_def2', component_property='value')],
    prevent_initial_call=False
)
def update_3d2(n_clicks, minutes_def2):
    with np.errstate(divide='ignore', invalid='ignore'):
        fig = go.Figure(
            data=[go.Surface(z=z, x=x, y=y, colorscale='blues', surfacecolor=np.zeros(90 * 80).reshape(90, 80)),
                  go.Surface(x=x, y=y, z=np.zeros(7200).reshape(90, 80),
                             surfacecolor=image_resized, colorscale='BuGn_r')],
            layout=layout)

        row = liverpool_off.iloc[minutes_def2]

        a = 1 / (np.sqrt((x + 0) ** 2 + (yt + 0) ** 2)) * row['a']
        b = 1 / (np.sqrt((x - 30) ** 2 + (yt + 0) ** 2)) * row['b']
        c = 1 / (np.sqrt((x - 60) ** 2 + (yt + 0) ** 2)) * row['c']
        d = 1 / (np.sqrt((x - 15) ** 2 + (yt - 40) ** 2)) * row['d']
        e = 1 / (np.sqrt((x - 45) ** 2 + (yt - 40) ** 2)) * row['e']
        f = 1 / (np.sqrt((x - 15) ** 2 + (yt + 40) ** 2)) * row['f']
        g = 1 / (np.sqrt((x - 45) ** 2 + (yt + 40) ** 2)) * row['g']

        A = a + b + c + d + e + f + g

        A[A > 100] = 100
        A[A < -100] = -100

        fig.data[0].z = A

        fig.update_layout(scene_aspectmode='manual',
                          scene_aspectratio=dict(x=1, y=1, z=1),
                          scene_camera=camera)

        #fig.update_layout(margin=dict(b=0, t=0))

        fig.update_layout(title='Liverpool [F.C. Women] Offensive (3D Surface)', title_x=0.08, title_y=0.925)

        fig.update_traces(showscale=False)

        return fig


@app.callback(
    Output(component_id='2D-graph2', component_property='figure'),
    Input(component_id='my_button2', component_property='n_clicks'),
    [State(component_id='minutes_def2', component_property='value')],
    prevent_initial_call=False
)
def update_2d2(n_clicks, minutes_def2):
    with np.errstate(divide='ignore', invalid='ignore'):
        fig2 = go.Figure(
            data=[
                go.Contour(z=z, showscale=True, connectgaps=True)],
            layout=layout2)

        row = liverpool_off.iloc[minutes_def2]

        a = 1 / (np.sqrt((x + 0) ** 2 + (yt + 0) ** 2)) * row['a']
        b = 1 / (np.sqrt((x - 30) ** 2 + (yt + 0) ** 2)) * row['b']
        c = 1 / (np.sqrt((x - 60) ** 2 + (yt + 0) ** 2)) * row['c']
        d = 1 / (np.sqrt((x - 15) ** 2 + (yt - 40) ** 2)) * row['d']
        e = 1 / (np.sqrt((x - 45) ** 2 + (yt - 40) ** 2)) * row['e']
        f = 1 / (np.sqrt((x - 15) ** 2 + (yt + 40) ** 2)) * row['f']
        g = 1 / (np.sqrt((x - 45) ** 2 + (yt + 40) ** 2)) * row['g']

        A = a + b + c + d + e + f + g

        A[A > 100] = 100
        A[A < -100] = -100

        #fig2.update_layout(margin=dict(b=0, t=0))
        fig2.update_layout(title='Liverpool [F.C. Women] Offensive (2D Contour)')


        fig2.data[0].z = A

        return fig2

if __name__ == '__main__':
    app.run_server(debug=True)
