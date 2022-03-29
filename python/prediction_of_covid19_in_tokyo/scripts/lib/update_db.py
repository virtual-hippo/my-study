from scripts.lib.constants import *
from scripts.lib.logger import Logger

import pandas as pd
import numpy as np
import sqlite3

def update_db():
    logger = Logger(__name__)
    raw_df = pd.read_csv(DATA_URL, usecols=EXTRACT_COLS, header=0)
    logger.info("csv file is downloaded")
    raw_df.to_csv(RAW_CSV_PATH)

    shaped_df = pd.DataFrame(columns=COLS)
    shaped_df.index.name = INDEX_NAME

    # データ成形
    for i, date in enumerate(raw_df[DATE].unique()):
        df_date = raw_df[raw_df[DATE] == date]
        tmp_array = [
            len(df_date),
            len(df_date[df_date[AGE] == "10歳未満"]),
            len(df_date[df_date[AGE] == "10代"]),
            len(df_date[df_date[AGE] == "20代"]),
            len(df_date[df_date[AGE] == "30代"]),
            len(df_date[df_date[AGE] == "40代"]),
            len(df_date[df_date[AGE] == "50代"]),
            len(df_date[df_date[AGE] == "60代"]),
            len(df_date[df_date[AGE] == "70代"]),
            len(df_date[(df_date[AGE] == "80代") | (df_date[AGE] == "90代") | (df_date[AGE] == "100歳以上")]),
            len(df_date[(df_date[AGE] == "不明") | (df_date[AGE] == "-")]),
            len(df_date[df_date[SEX] == "男性"]),
            len(df_date[df_date[SEX] == "女性"]),
            len(df_date[(df_date[SEX] == "-") | (df_date[SEX] == "―") | (df_date[SEX] == "不明")]),
            len(df_date) - shaped_df.iloc[i - 1, 0] if i != 0 else 0, # 前日との差分
            len(df_date) - shaped_df.iloc[i - 1, 0] - shaped_df.iloc[i - 1, len(COLS) - 2] if i != 0 else 0, # 前日との差分の差分
        ]
        shaped_df.loc[date] = tmp_array

    # db ファイル作成/更新
    file_sqlite3 = SHAPED_DB_PATH
    conn = sqlite3.connect(file_sqlite3)
    shaped_df.to_sql(TABLE_NAME, conn, if_exists="replace")
    logger.info("db file is updated")
    conn.close()