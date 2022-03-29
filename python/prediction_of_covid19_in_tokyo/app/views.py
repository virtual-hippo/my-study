from flask import Flask, render_template
import sqlite3
import pandas as pd

from scripts.lib.constants import SHAPED_DB_PATH, TABLE_NAME, INDEX_NAME, MODELS_PATH
from scripts.lib.update_db import update_db
from scripts.visualize_data import get_graph_json
from models.lstm import LSTMModel
from scripts.lib.logger import Logger

logger = Logger(__name__)
app = Flask(__name__)

# データ読み込み
logger.info("read db")
file_sqlite3 = SHAPED_DB_PATH
conn = sqlite3.connect(file_sqlite3)
df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME};", conn, index_col=INDEX_NAME,)
conn.close()

# 翌日の予測
logger.info("predict")
lstm = LSTMModel()
predict = lstm.predict_next_day(lstm.get_model())

graph_json = get_graph_json()

@app.route("/")
def index():
    # リストへ変換
    df_values = df.values.tolist()
    df_columns = df.columns.tolist()
    df_columns.insert(0, INDEX_NAME)
    df_index = df.index.tolist()

    return render_template("index.html",
                           title="Predict covid-19 in Tokyo",
                           predict=predict,
                           graph_json=graph_json,
                           values=df_values,
                           columns=df_columns,
                           index=df_index)

# ToDo: update db
#@app.route('/background_process_test')
#def background_process_test():
#    update_db()
#    return render_template("update_db.html")

# ToDo: train
#@app.route('/background_process_test')
#def background_process_test():
#    update_db()
#    return render_template("update_db.html")