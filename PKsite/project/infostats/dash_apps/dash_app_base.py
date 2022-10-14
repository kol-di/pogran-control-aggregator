from dash import html, dcc
import pandas as pd
from itertools import chain
from datetime import date, timedelta
from collections import defaultdict

from PKdb.db_locations import MongodbService


class DashAppHelper:
    _instance = None
    _df = None

    @classmethod
    def instantiate(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            db = MongodbService.get_instance()
            data = db.get_data()
            db.close_connection()
            assert len(data) > 0, 'No data in the database'
            cls._df = pd.DataFrame(data).explode('locations', ignore_index=True)
        return cls._instance

    @classmethod
    def get_selectors(cls):
        assert cls._instance is not None, "Instantiate class first"

        all_tag = 'Все'

        location_values = cls._df['locations'].values.tolist()
        location_values.insert(0, all_tag)

        transport_values = list(set(chain(*cls._df['transport'].tolist())))
        transport_values.insert(0, all_tag)

        min_date = cls._df['date'].min().date() + timedelta(days=1)
        max_date = cls._df['date'].max().date() - timedelta(days=1)

        html_selectors = \
            html.Div(children=[
                html.Div(children=[
                    html.Label('Location'),
                    dcc.Dropdown(
                        location_values,
                        all_tag,
                        multi=True,
                        id='dropdown-location'),

                    html.Br(),
                    html.Label('Transport'),
                    dcc.Dropdown(transport_values, all_tag, multi=True, id='dropdown-transport'),
                ], style={'padding': 10, 'flex': 1}),

                html.Div(children=[
                    html.Br(),
                    html.Label('Date'),
                    dcc.DatePickerRange(
                        min_date_allowed=min_date,
                        max_date_allowed=max_date,
                        start_date=min_date,
                        end_date=max_date,
                        initial_visible_month=date(2022, 10, 5),
                        updatemode='singledate',
                        display_format='DD.MM.YYYY',
                        id='date-picker',
                    )
                ], style={'padding': 10, 'flex': 1}),
            ], style={'display': 'flex', 'flex-direction': 'row'})

        return html_selectors

    @staticmethod
    def multi_select_values(vals, df_col):
        all_tag = 'Все'

        if not isinstance(vals, list):
            vals = [vals]
        if all_tag not in vals:
            # df_vals = set(chain(*df_col.tolist()))
            try:
                if isinstance(df_col[0], list):
                    val_obs = pd.Series([any(val in df_vals for val in vals) for
                                         df_vals in df_col.tolist()])
                else:
                    val_obs = pd.Series(df_col.isin(vals))
            except IndexError:
                val_obs = pd.Series([])

        else:
            val_obs = pd.Series([True] * len(df_col))

        return val_obs

    @classmethod
    def filter_data(cls, locations, transports, date_from, date_to):
        assert cls._instance is not None, "Instantiate class first"

        start_date = pd.to_datetime(date_from)
        end_date = pd.to_datetime(date_to)
        date_obs = (cls._df.date >= start_date) & (cls._df.date <= end_date)

        location_obs = cls.multi_select_values(locations, cls._df.locations)

        transport_obs = cls.multi_select_values(transports, cls._df.transport)

        dff = cls._df[location_obs & transport_obs & date_obs]

        return dff
