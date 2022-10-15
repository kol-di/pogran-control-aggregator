import pandas as pd
from django_plotly_dash import DjangoDash
from dash import html, dcc, Input, Output
import plotly.express as px
from datetime import timedelta

from .dash_app_base import DashAppHelper

app = DjangoDash(name='dynamics')

DashAppHelper.instantiate()

app.layout = html.Div(
    children=[
        dcc.Graph(
            id='graph',
        ),

        dcc.Slider(
            min=1,
            max=5,
            step=1,
            value=1,
            id='slider'),

        DashAppHelper.get_selectors()
    ])


@app.callback(
    Output('graph', 'figure'),
    Input('dropdown-location', 'value'),
    Input('dropdown-transport', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('slider', 'value'))
def update_graph(locations, transports, date_from, date_to, interval):
    dff = DashAppHelper.filter_data(locations, transports, date_from, date_to)

    dff_groups = dff.groupby(pd.Grouper(
        key='date',
        axis=0,
        freq=str(interval) + 'D',
        sort=True))
    dff_dyn = (dff_groups.sum('refused') / dff_groups.count() * 100)
    dff_dyn = dff_dyn.rename(columns={'refused': 'Refuse Rate'})
    dff_dyn['Refuse Rate'] = dff_dyn['Refuse Rate'].round(1)

    fig = px.line(dff_dyn, x=dff_dyn.index, y='Refuse Rate')
    fig.update_layout(transition_duration=200)

    return fig
