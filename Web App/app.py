import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output, State
# import numpy as np

import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import plotly.offline as py
from ipywidgets.embed import embed_minimal_html

from ipywidgets import interactive, HBox, VBox
from ipywidgets import FloatSlider, IntSlider

layout = go.Layout(
        scene=dict(
            xaxis=dict(
                nticks=8, range=[-10, 70], ),
            yaxis=dict(
                nticks=8, range=[-80, 80], ),
            zaxis=dict(
                nticks=9, range=[-60, 100], ), ))

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
server = app.server


app.layout = html.Div(
    [
    dbc.Row([
            dbc.Col(html.Div([
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            dcc.Loading(id="loading-1",
                                        children=[dcc.Graph(id='3D-graph', figure={})])]), md=7),
            dbc.Col(html.Div([
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Label([html.Strong('a: '),
                                #dcc.Input(id='a', type='number', step=0.1, value=0.5),
                                dcc.Slider(
                                        id='a',
                                        min=-50,
                                        max=50,
                                        step=0.1,
                                        value=0.5,
                                    ),
                                html.Div(id='slider-drag-output', style={'margin-top': -20,'margin-left':26})
                                ]),
                    html.Br(),
                    html.Label([html.Strong('b: '),
                                #dcc.Input(id='b', type='number', step=0.1, value=2.2)]),
                                dcc.Slider(
                                        id='b',
                                        min=-50,
                                        max=50,
                                        step=0.1,
                                        value=2.2,
                                    ),
                                html.Div(id='slider-drag-output2', style={'margin-top': -20,'margin-left':26})
                                ]),
                    html.Br(),
                    html.Label([html.Strong('c: '),
                                #dcc.Input(id='c', type='number', step=0.1, value=7.3),
                                dcc.Slider(
                                    id='c',
                                    min=-50,
                                    max=50,
                                    step=0.1,
                                    value=7.3,
                                ),
                                html.Div(id='slider-drag-output3', style={'margin-top': -20,'margin-left':26})
                                ]),
                    html.Br(),
                    html.Label([html.Strong('d: '),
                                #dcc.Input(id='d', type='number', step=0.1, value=3.8),
                                dcc.Slider(
                                    id='d',
                                    min=-50,
                                    max=50,
                                    step=0.1,
                                    value=3.8,
                                ),
                                html.Div(id='slider-drag-output4', style={'margin-top': -20,'margin-left':26})
                                ]),
                    html.Br(),
                    html.Label([html.Strong('e: '),
                                #dcc.Input(id='e', type='number', step=0.1, value=3.7),
                                dcc.Slider(
                                    id='e',
                                    min=-50,
                                    max=50,
                                    step=0.1,
                                    value=3.7,
                                ),
                                html.Div(id='slider-drag-output5', style={'margin-top': -20,'margin-left':26})
                                ]),
                    html.Br(),
                    html.Label([html.Strong('f: '),
                                #dcc.Input(id='f', type='number', step=0.1, value=12.2),
                                dcc.Slider(
                                    id='f',
                                    min=-50,
                                    max=50,
                                    step=0.1,
                                    value=12.2,
                                ),
                                html.Div(id='slider-drag-output6', style={'margin-top': -20,'margin-left':26})
                                ]),
                    html.Br(),
                    html.Br(),
                    html.Label(
                        dbc.Button(id='my_button', n_clicks=0, children="Submit", color="success"),
                        style={'font-weight': 'bold'}),
                    html.Br()
                ]), md=5)
            ])
    ])

    # html.Div([
    #     dcc.Graph(
    #         id='3D-graph',
    #         figure={})]),
    # html.Br(),
    # html.Label(["a: ",
    #             dcc.Input(id='a', type='number', step=0.1, value=0.5)]),
    # html.Br(),
    # html.Label(["b: ",
    #             dcc.Input(id='b', type='number', step=0.1, value=2.2)]),
    # html.Br(),
    # html.Label(["c: ",
    #             dcc.Input(id='c', type='number', step=0.1, value=7.3)]),
    # html.Br(),
    # html.Label(["d: ",
    #             dcc.Input(id='d', type='number', step=0.1, value=3.8)]),
    # html.Br(),
    # html.Label(["e: ",
    #             dcc.Input(id='e', type='number', step=0.1, value=3.7)]),
    # html.Br(),
    # html.Label(["f: ",
    #             dcc.Input(id='f', type='number', step=0.1, value=12.3)]),
    # html.Br(),
    # html.Br(),
    # html.Label(
    #     dbc.Button(id='my_button', n_clicks=0, children="Submit", color="primary",
    #                size="lg"),
    #     style={'font-weight': 'bold'}),
    # html.Br()], style={'text-align': 'center'})

@app.callback(Output('slider-drag-output', 'children'),
              [Input('a', 'drag_value'), Input('a', 'value')])
def display_value(drag_value, value):
    return 'drag_value: {} | value: {}'.format(value, value)

@app.callback(Output('slider-drag-output2', 'children'),
              [Input('b', 'drag_value'), Input('b', 'value')])
def display_value(drag_value, value):
    return 'drag_value: {} | value: {}'.format(value, value)

@app.callback(Output('slider-drag-output3', 'children'),
              [Input('c', 'drag_value'), Input('c', 'value')])
def display_value(drag_value, value):
    return 'drag_value: {} | value: {}'.format(value, value)

@app.callback(Output('slider-drag-output4', 'children'),
              [Input('d', 'drag_value'), Input('d', 'value')])
def display_value(drag_value, value):
    return 'drag_value: {} | value: {}'.format(value, value)

@app.callback(Output('slider-drag-output5', 'children'),
              [Input('e', 'drag_value'), Input('e', 'value')])
def display_value(drag_value, value):
    return 'drag_value: {} | value: {}'.format(value, value)

@app.callback(Output('slider-drag-output6', 'children'),
              [Input('f', 'drag_value'), Input('f', 'value')])
def display_value(drag_value, value):
    return 'drag_value: {} | value: {}'.format(value, value)


@app.callback(
    Output(component_id='3D-graph', component_property='figure'),
    Input(component_id='my_button', component_property='n_clicks'),
    [State(component_id='a', component_property='value'),
     State(component_id='b', component_property='value'),
     State(component_id='c', component_property='value'),
     State(component_id='d', component_property='value'),
     State(component_id='e', component_property='value'),
     State(component_id='f', component_property='value')],
    prevent_initial_call=False
)
def update_z(n_clicks, a, b, c, d, e, f):
    with np.errstate(divide='ignore', invalid='ignore'):
        x = np.arange(-10, 70)
        y = np.arange(-80, 80)
        yt = np.array([[i] for i in y])
        z = x * yt

        # fig = go.Figure(
        #     data=[
        #         go.Contour(z=z, x=x, y=y, )],
        #     layout=layout)

        fig = go.Figure(
            data=[
                go.Contour(z=z, showscale=True, connectgaps=True)],
            layout=layout)

        camera = dict(
            eye=dict(x=1.75, y=1, z=0.1)
        )
        otherback = -(e / (np.sqrt(((20 + x) / yt) ** 2 + (yt / 100) ** 2))) - \
                    (f / (np.sqrt(((20 + x) / 10) ** 2 + (yt / 5) ** 2)))

        quicktest2 = -(c / (np.sqrt(((100 - x) / (2 * yt)) ** 2 + ((40 - yt) / 20) ** 2))) - \
                     (d / (np.sqrt(((100 - x) / (2 * yt)) ** 2 + ((40 + yt) / 20) ** 2)))

        fronttest2 = -(5 * a / (np.sqrt(((70 - x) / 10) ** 2 + (yt / 7) ** 2))) - \
                     (b / (np.sqrt(((70 - x) / yt) ** 2 + (yt / 10) ** 2)))

        setupthree = fronttest2 + quicktest2 + otherback

        fig.data[0].z = setupthree

        #fig.update_traces(showscale=False)
        fig.update_layout(margin=dict(b=0, t=0))

        fig.update_layout(scene_camera=camera)

        # fig.update_traces(contours_z=dict(show=True, usecolormap=True,
        #                                   highlightcolor="limegreen", project_z=True))
        # fig.update_layout(title='3D Surface Plot', autosize=False,
        #                   scene_camera_eye=dict(x=1.87, y=0.88, z=-0.64),
        #                   width=500, height=500,
        #                   margin=dict(l=65, r=50, b=65, t=90))

        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
