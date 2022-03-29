# 使用データ
use_cols = ["2nd_order_diff"]
length_of_sequence = 30
use_date = "2020-03-22"

# 学習
latent_dim = 64
learning_rate = 0.01
batch_size = 50
epochs = 200
activation = "linear"
load_weights = False
split_size = 5
dropout_rate = 0.5

# 環境
ip = "127.0.0.1"
port = "8080"
debug = True