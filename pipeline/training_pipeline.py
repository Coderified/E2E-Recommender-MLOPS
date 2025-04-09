# Merge all the steps in src to create a pipeline
from config.paths_config import *
from utils .common_functions import read_yaml

from src.data_processing import DataProcessing
from src.modeltraining import ModelTraining

#Data ingestion not here
#data ingestion does GCP to PC

# ALL things inartifacts folder will be pusehd to another gcp bucket
# when we need artifcats,we do that with DVC, so data ingestion comes there

if __name__ == "__main__":

    data_processor = DataProcessing(ANIME_LIST_CSV,PROCESSED_DIR)
    data_processor.run()

    model_trainer = ModelTraining(PROCESSED_DIR)
    model_trainer.model_training()