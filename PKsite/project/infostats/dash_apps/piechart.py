from django_plotly_dash import DjangoDash
from dash import html, dcc, Input, Output
import plotly.express as px

from .dash_app_base import DashAppHelper

app = DjangoDash(name='piechart')

DashAppHelper.instantiate()

app.layout = html.Div(
    children=[
        dcc.Graph(
            id='graph',
        ),

        DashAppHelper.get_selectors()
    ])


@app.callback(
    Output('graph', 'figure'),
    Input('dropdown-location', 'value'),
    Input('dropdown-transport', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'))
def update_graph(locations, transports, date_from, date_to):
    dff = DashAppHelper.filter_data(locations, transports, date_from, date_to)

    fig = px.pie(values=dff['refused'].value_counts(), names=dff['refused'].unique())
    fig.update_layout(legend=dict(font=dict(size=20, color="black"), title='Refused'))
    fig.update_layout(transition_duration=200)

    return fig
