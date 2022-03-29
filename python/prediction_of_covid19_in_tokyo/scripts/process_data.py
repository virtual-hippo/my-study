from scripts.lib.constants import *
from config import config as cfg

import pandas as pd
import numpy as np
import sqlite3
from sklearn.preprocessing import StandardScaler

class DataProcesser:
    def __init__(self):
        self._df, self._label = self._read_data()

    def _read_data(self):
        # データ読み込み
        file_sqlite3 = SHAPED_DB_PATH
        conn = sqlite3.connect(file_sqlite3)
        df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME};", conn, index_col=INDEX_NAME,)
        conn.close()

        # 使用する列のみ抜き出す
        # 設定した日付以降のみ抜き出す
        ret_df = df.loc[cfg.use_date:, cfg.use_cols]

        # ラベルの抜き出し
        label = df.loc[cfg.use_date:, LABEL].values
        reshape_label = label.reshape(len(label), 1)

        return ret_df, reshape_label

    def _standardize(self, value):
        # 標準化
        std_scl = StandardScaler()
        std_scl.fit(value)

        return std_scl.transform(value)

    def load_dataset(self):
        # 標準化
        standardized_data = self._standardize(self._df.values)
        standardized_label = self._standardize(self._label)

        # データセット作成
        train_data = []
        label = []
        for i in range(len(standardized_data) - cfg.length_of_sequence):
            train_data.append([rows for rows in standardized_data[i:i + cfg.length_of_sequence]])
            label.append(standardized_label[i + cfg.length_of_sequence][0])
        
        # (データ数, 入力行数, 入力列数)に成形
        re_train_data = np.array(train_data).reshape(len(train_data), cfg.length_of_sequence, len(cfg.use_cols))
        # (データ数, 1)に成形
        re_label = np.array(label).reshape(len(label), 1)

        return re_train_data, re_label

    def load_recent_data(self):
        # 標準化
        standardized_data = self._standardize(self._df.values)

        # データセット作成
        recent_data = standardized_data[-cfg.length_of_sequence:]

        return recent_data
    
    def get_update_date(self):
        # 最新の日付を返す
        return self._df.index[-1]

    def inverse_transform_predictions(self, predictions):
        # 標準化を戻す
        std_scl = StandardScaler()
        std_scl.fit(self._label)
        
        return std_scl.inverse_transform(predictions)