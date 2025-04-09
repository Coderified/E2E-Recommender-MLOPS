import os
import pandas as pd
from google.cloud import storage
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml


logger = get_logger(__name__)

class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]  #from config.yaml the it is read and stored
        self.bucket_name = self.config["bucket_name"] #from config.yaml the it is read and stored
        self.file_names = self.config["bucket_file_names"] #from config.yaml the it is read and stored

        os.makedirs(RAW_DIR,exist_ok=True)
        logger.info(f"Data Integration started with {self.bucket_name}")

    def download_data(self):
        try:
            logger.info("Client and bucket init")

            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            
            logger.info("Looping to identify small and big files")
            for filename in self.file_names:
                file_path = os.path.join(RAW_DIR,filename)

                if filename =="animelist.csv":
                    #A blob (Binary Large Object) in GCS represents an individual file 
                    #stored in your bucket. When you create a blob object, you're essentially creating a reference to a file location in your cloud storage
                    blob = bucket.blob(filename)  
                    blob.download_to_filename(file_path)

                    data = pd.read_csv(file_path,nrows=5000000)
                    data.to_csv(file_path,index=False)
                    logger.info("Large file parsed and only downloading 5M rows")
                else:
                    blob = bucket.blob(filename)
                    blob.download_to_filename(file_path)
                    logger.info("Downloading smaller files")

        except Exception as e:
            logger.error("Error reading and downloading files from GC Buckets")
            raise CustomException("Failed to download data",e)

    def run(self):
        try:
            logger.info("Starting data ingestion process")
            self.download_data()
            logger.info("Data download done")

        except CustomException as ce:
            logger.error(f"Custom Exception:{str(ce)}")

        finally:
            logger.info("Data Ingestion py reached")

if __name__ == "__main__":
    dataingestion = DataIngestion(read_yaml(CONFIG_PATH))
    dataingestion.run()



