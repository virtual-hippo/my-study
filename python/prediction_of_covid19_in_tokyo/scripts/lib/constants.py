DATA_URL = "https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv"
EXTRACT_COLS = ["公表_年月日", "患者_年代", "患者_性別"]
DATE = "公表_年月日"
AGE = "患者_年代"
SEX = "患者_性別"
COLS = ["num", "under10", "10s", "20s", "30s", "40s", "50s", "60s", "70s", "80s-", "unknown_age", "male", "female", "unknown_sex", "diff", "2nd_order_diff"]
INDEX_NAME = "date"
LABEL = "num"

SHAPED_DB_PATH = "./data/input/shaped_data.db"
RAW_CSV_PATH = "./data/input/tokyo_covid19_patients.csv"
TABLE_NAME = "tokyo_covid19_patients"
LOG_DIR = "./log/"
CONF_PATH = "./config/config.ini"
WEIGHTS_PATH = "./data/output/weights/lstm_weights.h5"
MODELS_PATH = "./data/output/models/lstm_models.h5"
HISTORY_PATH = "./data/output/history/lstm_history.csv"
HISTORY_DIR = "./data/output/history/"