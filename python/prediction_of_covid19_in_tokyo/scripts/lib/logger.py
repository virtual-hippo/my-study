from logging import FileHandler, StreamHandler, Formatter, handlers, getLogger, DEBUG, INFO
from scripts.lib.constants import LOG_DIR

import datetime
import os

class Logger:
    def __init__(self, name, log_level=DEBUG):
        self.logger = getLogger(name)
        self.logger.setLevel(log_level)

        # ログファイル用
        file_formatter = Formatter(fmt="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", datefmt="%Y/%m/%d %H:%M:%S")
        date = datetime.datetime.now().strftime("%Y%m%d")
        file_handler = FileHandler(os.path.join(LOG_DIR, f"{date}.log"))
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(DEBUG)
        self.logger.addHandler(file_handler)

        # 標準出力用
        st_formatter = Formatter(fmt="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", datefmt="%H:%M:%S")
        st_handler = StreamHandler()
        st_handler.setFormatter(st_formatter)
        st_handler.setLevel(INFO)
        self.logger.addHandler(st_handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg, exc_info):
        self.logger.error(msg, exc_info=exc_info)

    def critical(self, msg):
        self.logger.critical(msg)