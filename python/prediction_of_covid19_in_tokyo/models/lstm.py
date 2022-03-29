from scripts.lib.constants import *
from scripts.lib.logger import Logger
from scripts.process_data import DataProcesser
from config import config as cfg

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


class LSTMModel:
    def __init__(self):
        self.logger = Logger(__name__)
        self._data_processer = DataProcesser()

    def _create_model(self, length_of_sequence, input_dim):
        inputs = Input(shape=(length_of_sequence, input_dim))
        lstm = LSTM(cfg.latent_dim, activation="tanh", recurrent_activation="sigmoid", return_sequences=False)(inputs)
        debse1 = Dense(cfg.latent_dim, activation="relu")(lstm)
        dropout1 = Dropout(cfg.dropout_rate, noise_shape=None, seed=None)(debse1)
        debse2 = Dense(cfg.latent_dim, activation="relu")(lstm)
        dropout2 = Dropout(cfg.dropout_rate, noise_shape=None, seed=None)(debse2)
        predictions = Dense(1, activation=cfg.activation)(dropout2)

        model = Model(inputs=inputs, outputs=predictions)
        optimizer = Adam(learning_rate=cfg.learning_rate)
        model.compile(loss="mean_squared_error", optimizer=optimizer, metrics=["mae"])
        model.summary()

        return model

    def _train(self, x, y, validation_data, model):
        # callbackリスト作成
        callbacks = [
            EarlyStopping(monitor='val_loss',
                          mode='auto',
                          patience=30,
                          restore_best_weights=True
                        ),
            ModelCheckpoint(WEIGHTS_PATH,
                            monitor='val_loss',
                            verbose=0,
                            save_best_only=True,
                            save_weights_only=False,
                            mode='auto',
                        )
            ]

        # 重みファイル読み込み
        if os.path.exists(WEIGHTS_PATH) and cfg.load_weights:
            try: 
                self.logger.info("load weights")
                model.load_weights(WEIGHTS_PATH)
            except ValueError as e:
                self.logger.error("can't load weights", e)

        # 学習
        history = model.fit(x, y,
            batch_size=cfg.batch_size,
            epochs=cfg.epochs,
            validation_data=validation_data,
            callbacks=callbacks
            )

        # モデル保存
        model.save(MODELS_PATH)

        return history.history

    def _evaluate(self, X_test, y_test, model):
        score = model.evaluate(X_test, y_test, verbose=0)
        self.logger.info(f"[score]  loss:{score[0]} mae:{score[1]}")

        return score
    
    def _predict(self, X, model):
        # 重みファイル読み込み
        if os.path.exists(WEIGHTS_PATH):
            try: 
                self.logger.info("load weights")
                model.load_weights(WEIGHTS_PATH)
            except ValueError as e:
                self.logger.error("can't load weights", e)
        else:
            self.logger.info("weights file doesn't exist")
        predictions = model.predict(X)
        inverse_predictions = self._data_processer.inverse_transform_predictions(predictions)

        return inverse_predictions

    def predict_next_day(self, model):
        # 重みファイル読み込み
        if os.path.exists(WEIGHTS_PATH):
            try: 
                self.logger.info("load weights")
                model.load_weights(WEIGHTS_PATH)
            except ValueError as e:
                self.logger.error("can't load weights", e)
        else:
            self.logger.info("weights file doesn't exist")

        X = self._data_processer.load_recent_data()
        update_date = self._data_processer.get_update_date()
        prediction = model.predict(X[np.newaxis, ...])
        inverse_prediction = self._data_processer.inverse_transform_predictions(prediction) # ndarray (1,1)
        next_day = update_date[:-2] + str(int(update_date[-2:]) + 1).zfill(2) # str
        self.logger.info(f"{next_day}: {inverse_prediction[0][0]}")

        return (next_day, int(inverse_prediction[0][0]))

    def _save_history(self, history):
        self.logger.info("save_history")
        # 学習履歴保存
        hist_df = pd.DataFrame(history)
        hist_df.to_csv(HISTORY_PATH)

        # 学習曲線作成
        # mae
        plt.figure()
        hist_df[['mae', 'val_mae']].plot()
        plt.ylabel('mae')
        plt.xlabel('epoch')
        plt.savefig(os.path.join(HISTORY_DIR, 'mae.png'))
        plt.close()
        
        # loss
        plt.figure()
        hist_df[['loss', 'val_loss']].plot()
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.savefig(os.path.join(HISTORY_DIR, 'loss.png'))
        plt.close()

    def get_model(self):
        self.logger.debug("load_model")

        return load_model(MODELS_PATH)

    
    def run(self):
        train_data, label = self._data_processer.load_dataset()
        # 学習データと教師データに分割
        X_train, X_test, y_train, y_test = train_test_split(train_data, label, test_size=0.25, random_state=5)

        # 入力行数と列数を取得
        _, length_of_sequence, input_dim = X_train.shape # _はデータ数

        # モデル作成
        model = self._create_model(length_of_sequence=length_of_sequence, input_dim=input_dim)

        # 学習
        self.logger.info("start training")

        # k交差分割検証
        kf = KFold(n_splits=cfg.split_size)
        for idx, (train_idx, val_idx) in enumerate(kf.split(X_train, y_train)):
            train_data = X_train[train_idx]                 # 訓練データ
            train_label = y_train[train_idx]                # 訓練ラベル
            val_data = (X_train[val_idx], y_train[val_idx]) # 検証データ
            history = self._train(train_data, train_label, val_data, model)
            # 学習履歴保存
            if idx == 0 and not cfg.load_weights:
                self._save_history(history)
            # 評価
            self._evaluate(X_test, y_test, model)

        # 予測
        self.predict_next_day(model)
        