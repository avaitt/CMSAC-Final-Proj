import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.io as pio
import plotly
import plotly.express as px
import json
import pickle
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import skimage.io as sio
from skimage.transform import rescale, resize, downscale_local_mean
from skimage.filters import unsharp_mask

image = sio.imread("soccer_fieldv3.jpeg")
img = image[:, :, 1]
#t2 = img[:, int(img.shape[1] / 2):]

image_rescaled = rescale(img, 0.25, anti_aliasing=False)
image_resized = resize(image_rescaled, (92, 140), anti_aliasing=True)
image_final = unsharp_mask(image_resized, radius=30, amount=1)

arsenal_def = pd.read_csv('19770/Arsenal_WFC_Defense_Coef.csv')
manchester_off = pd.read_csv('19770/Manchester_City WFC_Offennse_Coef.csv')

x = np.arange(-10,130)
y = np.arange(-45,45)
yt = np.array([[i] for i in y])
z = x * yt

layout = go.Layout(
        scene = dict(
        xaxis = dict(
        nticks=14, range = [-10,130],),
        yaxis = dict(
        nticks=8, range = [-45,45],),
        zaxis = dict(
        nticks=20, range = [-1000,1000],),),
    # margin=dict(
    #     t=0, # top margin: 30px, you want to leave around 30 pixels to
    #           # display the modebar above the graph.
    #     b=10, # bottom margin: 10px
    #     l=20, # left margin: 10px
    #     r=20, # right margin: 10px
    # ),
        margin=dict(
            t=50,  # top margin: 30px, you want to leave around 30 pixels to
            # display the modebar above the graph.
            b=10,  # bottom margin: 10px
            l=0,  # left margin: 10px
            r=10,  # right margin: 10px
        ),
        width=700,height=600)

layout2 = go.Layout(
        scene = dict(
        xaxis = dict(
        nticks=14, range = [-10,130],),
        yaxis = dict(
        nticks=8, range = [-45,45],),
        zaxis = dict(
        nticks=20, range = [-1000,1000],),),
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
            b=0,  # bottom margin: 10px
            l=80,  # left margin: 10px
            r=10,  # right margin: 10px
        ),
        width=550, height=500)

# camera = dict(
#     eye=dict(x=1.75, y=1, z=0.35)
# )

camera = dict(
    eye=dict(x=0, y=-1.5, z=1.7)
)

with np.errstate(divide='ignore', invalid='ignore'):
    def place_hole(x_loc, y_loc):
        return 1 / (np.sqrt((x - x_loc) ** 2 + (yt - y_loc) ** 2))

    phi1 = place_hole(-5, 0)  # a
    phi2 = place_hole(30, 0)  # b
    phi3 = place_hole(60, 0)  # c
    phi4 = place_hole(90, 0)  # d
    phi5 = place_hole(125, 0)  # e
    phi6 = place_hole(15, 40)  # f
    phi7 = place_hole(45, 40)  # g
    phi8 = place_hole(75, 40)  # h
    phi9 = place_hole(105, 40)  # i
    phi10 = place_hole(15, -40)  # j
    phi11 = place_hole(45, -40)  # k
    phi12 = place_hole(75, -40)  # l
    phi13 = place_hole(105, -40)  # m

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
server = app.server

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.Div([
            dcc.Graph(id='2D-graph', figure={})
        ], className='four columns'),
        html.Div([
            dcc.Graph(id='3D-graph', figure={})
            # html.Iframe(src=app.get_asset_url("test2.html"), width=600, height=400)
        ], className='four columns'),
        html.Div([
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Label([html.Strong('Minutes: '),
                        # dcc.Input(id='a', type='number', step=0.1, value=0.5),
                        dcc.Interval(
                            id='interval',
                            interval=800,
                            n_intervals=0,
                            max_intervals=45,
                            disabled=True
                        ),
                        dcc.Slider(
                            id='minutes_def',
                            min=0,
                            max=45,
                            step=1,
                            value=0),
                        html.Div(id='slider-drag-output',
                                 style={'margin-top': -20, 'margin-left': 26, 'padding-right': '140px'}),
                        html.Br(),
                        # html.Button('Play', id='my_btn')]),
                        html.Label(
                            dbc.Button(id='my_btn', n_clicks=0, children="Play", color="primary"),
                            style={'font-weight': 'bold', 'margin-left': 3}),
                        ]),
            html.Br(),
            html.Br()
            # html.Label(
            #     dbc.Button(id='my_button', n_clicks=0, children="Submit", color="success"),
            #     style={'font-weight': 'bold'}),
            # html.Br()
        ], className='four columns'),
    ], className='row')
])

@app.callback([Output('interval', 'disabled'), Output('my_btn', 'children')],
              [Input('my_btn', 'n_clicks')],
              [State('interval', 'disabled')])
def display_value(click, value):
    # print('click', value)
    if click:
        new_value = not value
        btn_name = 'Play' if new_value else 'Pause'
        return new_value, btn_name

    else:
        raise PreventUpdate


@app.callback(Output('minutes_def', 'value'),
              [Input('interval', 'n_intervals')])
def update_slider(num):
    return num


@app.callback(Output('slider-drag-output', 'children'),
              [Input('minutes_def', 'value')])
def display_val(value):
    return 'Timestep: {} minutes'.format(value)


@app.callback(
    Output(component_id='3D-graph', component_property='figure'),
    Input(component_id='minutes_def', component_property='value'),
    [State(component_id='minutes_def', component_property='value')]
)
def update_3d(n_clicks, minutes_def):
    with np.errstate(divide='ignore', invalid='ignore'):

        fig = go.Figure(
            data=[go.Surface(z=z, x=x, y=y),
                  go.Surface(x=x, y=y, z=np.zeros(12880).reshape(92, 140),
                             surfacecolor=image_final, colorscale='greens_r')],
            layout=layout)

        row = arsenal_def.iloc[minutes_def]

        row2 = manchester_off.iloc[minutes_def]

        a = phi1 * (row['a'] + row2['a'])
        b = phi2 * (row['b'] + row2['b'])
        c = phi3 * (row['c'] + row2['c'])
        d = phi4 * (row['d'] + row2['d'])
        e = phi5 * (row['e'] + row2['e'])
        f = phi6 * (row['f'] + row2['f'])
        g = phi7 * (row['g'] + row2['g'])
        h = phi8 * (row['h'] + row2['h'])
        i = phi9 * (row['i'] + row2['i'])
        j = phi10 * (row['j'] + row2['j'])
        k = phi11 * (row['k'] + row2['k'])
        l = phi12 * (row['l'] + row2['l'])
        m = phi13 * (row['m'] + row2['m'])

        A = a + b + c + d + e + f + g + h + i + j + k + l + m

        largest = np.nanmax(A[A != np.inf])
        smallest = np.nanmin(A[A != -np.inf])

        #     A[A > largest] = largest
        #     A[A < smallest] = smallest
        A[A == largest] = 1000
        A[A == smallest] = -1000

        A[A > 1000] = 1000
        A[A < -1000] = -1000

        fig.data[0].z = A

        fig.update_layout(scene_aspectmode='manual',
                          scene_aspectratio=dict(x=1, y=1, z=1),
                          scene_camera=camera)


        fig.update_layout(title='3D Surface of Manchester_City WFC and Arsenal WFC', title_x=0.14, title_y=0.925)

        fig.update_traces(showscale=False)

        return fig


# @app.callback(
#     Output(component_id='2D-graph', component_property='figure'),
#     Input(component_id='my_button', component_property='n_clicks'),
#     [State(component_id='minutes_def', component_property='value')],
#     prevent_initial_call=False
# )

@app.callback(
    Output(component_id='2D-graph', component_property='figure'),
    Input(component_id='minutes_def', component_property='value'),
    [State(component_id='minutes_def', component_property='value')]
)
def update_2d(n_clicks, minutes_def):
    with np.errstate(divide='ignore', invalid='ignore'):
        fig2 = go.Figure(
            data=[
                go.Contour(x=x, y=y, z=z, showscale=True, connectgaps=True)],
            layout=layout2)

        row = arsenal_def.iloc[minutes_def]

        row2 = manchester_off.iloc[minutes_def]

        a = phi1 * (row['a'] + row2['a'])
        b = phi2 * (row['b'] + row2['b'])
        c = phi3 * (row['c'] + row2['c'])
        d = phi4 * (row['d'] + row2['d'])
        e = phi5 * (row['e'] + row2['e'])
        f = phi6 * (row['f'] + row2['f'])
        g = phi7 * (row['g'] + row2['g'])
        h = phi8 * (row['h'] + row2['h'])
        i = phi9 * (row['i'] + row2['i'])
        j = phi10 * (row['j'] + row2['j'])
        k = phi11 * (row['k'] + row2['k'])
        l = phi12 * (row['l'] + row2['l'])
        m = phi13 * (row['m'] + row2['m'])

        A = a + b + c + d + e + f + g + h + i + j + k + l + m

        largest = np.nanmax(A[A != np.inf])
        smallest = np.nanmin(A[A != -np.inf])

        #     A[A > largest] = largest
        #     A[A < smallest] = smallest
        A[A == largest] = 1000
        A[A == smallest] = -1000

        A[A > 1000] = 1000
        A[A < -1000] = -1000

        fig2.data[0].z = A

        fig2.update_layout(scene_aspectmode='manual',
                           scene_aspectratio=dict(x=1, y=1, z=1))

        fig2.update_layout(title='2D Contour of Manchester_City WFC and Arsenal WFC', title_x=0.08, title_y=0.925)

    return fig2


if __name__ == '__main__':
    app.run_server(debug=True)
