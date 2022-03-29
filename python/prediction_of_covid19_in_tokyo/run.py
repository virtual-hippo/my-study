from scripts.lib.constants import *
from scripts.lib.logger import Logger
from scripts.lib.update_db import update_db
from config import config as cfg
from app.views import app, lstm

logger = Logger(__name__)

if __name__ == "__main__":
    logger.debug("start program")
    #update_db()
    #from scripts.process_data import DataProcesser
    #data_processer = DataProcesser()
    #data_processer.load_dataset()
    #from models.lstm import LSTMModel
    #lstm = LSTMModel()
    #lstm.run()
    app.run(host=cfg.ip, port=cfg.port, debug=cfg.debug)
