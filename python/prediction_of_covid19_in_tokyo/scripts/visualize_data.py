from scripts.lib.constants import SHAPED_DB_PATH, TABLE_NAME, INDEX_NAME

import pandas as pd
import sqlite3
import json
import plotly.offline as po
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder

class DataVisualizer:
    def __init__(self):
        self._df = self._read_data()

    def _read_data(self):
        # データ読み込み
        file_sqlite3 = SHAPED_DB_PATH
        conn = sqlite3.connect(file_sqlite3)
        df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME};", conn, index_col=INDEX_NAME,)
        conn.close()

        return df

    def create_traces(self):
        traces = []
        traces.append(go.Bar(x=self._df.index, y=self._df["num"], name="新規陽性者数"))

        return traces

    def create_fig(self, traces):
        fig = go.Figure(data=traces)

        return fig

def get_graph_json():
    data_visualizer = DataVisualizer()
    traces = data_visualizer.create_traces()
    fig = data_visualizer.create_fig(traces)
    graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)

    return graph_json