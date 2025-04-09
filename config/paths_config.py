#will list all the paths 

import os

#PAths for data ingestion
# we wannt to store data in 'raw' folder in artifacts

RAW_DIR = "artifacts/raw"
RAW_FILE_PATH = os.path.join(RAW_DIR,"")

#path to config yaml
CONFIG_PATH = "config/config.yaml"

#path to store processed data
PROCESSED_DIR = "artifacts/processed"
ANIME_LIST_CSV = "artifacts/raw/animelist.csv"
ANIME_CSV = "artifacts/raw/anime.csv"
ANIMESYNOPSIS_CSV = "artifacts/raw/anime_with_synopsis.csv"

X_TRAIN_ARRAY = os.path.join(PROCESSED_DIR,"X_train_array.pkl")
X_TEST_ARRAY = os.path.join(PROCESSED_DIR,"X_test_array.pkl")
Y_TRAIN = os.path.join(PROCESSED_DIR,"y_train.pkl")
Y_TEST = os.path.join(PROCESSED_DIR,"y_test.pkl")


RATING_DF = os.path.join(PROCESSED_DIR,"rating_df.csv")

DF = os.path.join(PROCESSED_DIR,"anime_df.csv")
SYNOPSIS_DF = os.path.join(PROCESSED_DIR,"anime_synopsis_df.csv")

USER2USER_ENCODED = "artifacts/processed/user2user_encoded.pkl"
USER2USER_DECODED = "artifacts/processed/user2user_decoded.pkl"

ANIME2ANIME_ENCODED = "artifacts/processed/anim2anime_encoded.pkl"
ANIME2ANIME_DECODED = "artifacts/processed/anim2anime_decoded.pkl"



#MODel Training paths
MODEL_DIR = "artifacts/model"   
WEIGHTS_DIR = "artifacts/weights"
MODEL_PATH = os.path.join(MODEL_DIR,"model.h5") 
ANIME_WEIGHTS_PATH = os.path.join(WEIGHTS_DIR,"anime_weights.pkl")
USER_WEIGHTS_PATH = os.path.join(WEIGHTS_DIR,"user_weights.pkl")
CHECKPOINT_FILE_PATH = "artifacts/model_checkpoint/weights.weights.h5"
