import joblib
import os
import sys
import pandas as pd
import numpy as np

import comet_ml

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, LearningRateScheduler

from src.logger import get_logger
from src.custom_exception import CustomException

from src.basemodel import BaseModel
from config.paths_config import *

logger = get_logger(__name__)

class ModelTraining():
    def __init__(self, data_path):
        self.data_path = data_path
        self.experiment = comet_ml.Experiment(api_key="hLdCSeTxQYtg2BMqIy1OWHbgs",
                                             project_name="mlops-recommender",
                                             workspace="coderified")
        logger.info("Model Training & Exprmt Tracker Comet Initialized")

    def load_data(self):
        try:
            x_train_array = joblib.load(X_TRAIN_ARRAY)
            x_test_array = joblib.load(X_TEST_ARRAY)
            y_train = joblib.load(Y_TRAIN)
            y_test  = joblib.load(Y_TEST)

            logger.info("Data loaded successfully")

            return x_train_array, x_test_array, y_train, y_test
        except Exception as e:
            raise CustomException("Error loading data", e) from e 

    def model_training(self):
        try:
            # Load data
            x_train_array, x_test_array, y_train, y_test=self.load_data()

            n_users = len(joblib.load(USER2USER_ENCODED))
            n_anime = len(joblib.load(ANIME2ANIME_ENCODED))

            # Load config
            config_path = CONFIG_PATH
            base_model = BaseModel(config_path) #basemodel class is initialized with the config path

            model = base_model.RecommenderNet(n_users, n_anime)
            logger.info("Model initialized successfully") #from basemodel we are getting the model instance
           
            start_lr = 0.0001 #Starting learning rate
            min_lr = 0.0001 #Minimum learning rate
            max_lr = 0.005 #Maximum learning rate
            batch_size = 10000 #Batch size

            ramup_epochs = 5 #Number of epochs
            sustain_epochs = 2 #Number of epochs to sustain the learning rate
            exponential_decay = 0.9 #Exponential decay rate


            def lrfn(epoch):
                if epoch < ramup_epochs:
                    lr = start_lr + (max_lr - start_lr) / ramup_epochs * epoch 
                elif epoch < ramup_epochs + sustain_epochs: 
                    lr = max_lr
                else:
                    lr = max_lr * exponential_decay ** (epoch - ramup_epochs - sustain_epochs)
                return lr

            lr_callback = LearningRateScheduler(lambda epoch: lrfn(epoch), verbose=0)
            #Learning rate scheduler to change the learning rate during training

            model_checkpoint = ModelCheckpoint(filepath=CHECKPOINT_FILE_PATH, save_weights_only=True, monitor='val_loss',
                                            mode='min', save_best_only=True, verbose=1) #Model checkpoint to save the best model weights

            early_stopping = EarlyStopping(monitor='val_loss', patience=3, verbose=1, mode='min', restore_best_weights=True) 
            #Early stopping to stop the training if the validation loss does not improve for 5 epochs

            my_callbacks = [lr_callback,early_stopping,model_checkpoint] #List of callbacks to be used during training
            
            os.makedirs(os.path.dirname(CHECKPOINT_FILE_PATH), exist_ok=True)
            #Create directory for model checkpoint
            os.makedirs(MODEL_DIR, exist_ok=True)   
            os.makedirs(WEIGHTS_DIR, exist_ok=True) 
            
            try:
                history = model.fit(
                        x=x_train_array,
                        y=y_train,
                        batch_size=batch_size,
                        epochs=20,
                        verbose=1,
                        validation_data = (x_test_array,y_test),
                        callbacks=my_callbacks
                    )
                model.load_weights(CHECKPOINT_FILE_PATH)
                logger.info("Model training Completedd.....") 



                for epoch in range(len(history.history['loss'])):
                    train_loss = history.history["loss"][epoch]
                    val_loss = history.history["val_loss"][epoch]

                    # Log metrics to Comet for each epoch
                    self.experiment.log_metric('train_loss',train_loss,step=epoch)
                    self.experiment.log_metric('val_loss',val_loss,step=epoch)
            
            except Exception as e:
                raise CustomException("Model training failed......",e)
            
            self.save_model_weights(model)

        except Exception as e:
            logger.error(str(e))
            raise CustomException("Error during Model Training Process",e)
        
    def extract_weights(self,layer_name,model):
        try:
            weight_layer = model.get_layer(layer_name)
            weights = weight_layer.get_weights()[0]
            weights = weights/np.linalg.norm(weights,axis=1).reshape((-1,1))
            logger.info(f"Extracting weights for {layer_name}")
            return weights
        except Exception as e:
            logger.error(str(e))
            raise CustomException("Error during Weight Extraction Process",e)

    def save_model_weights(self,model):
        try:
            model.save(MODEL_PATH)
            logger.info(f"Model saved to {MODEL_PATH}")

            user_weights = self.extract_weights('user_embedding',model)
            anime_weights = self.extract_weights('anime_embedding',model)

            joblib.dump(user_weights,USER_WEIGHTS_PATH)
            joblib.dump(anime_weights,ANIME_WEIGHTS_PATH)

            # For each experimentation we store the model and weights in the comet experiment
            self.experiment.log_asset(MODEL_PATH)
            self.experiment.log_asset(ANIME_WEIGHTS_PATH)
            self.experiment.log_asset(USER_WEIGHTS_PATH)

            logger.info("User and Anime weights saved sucesfully....")
        except Exception as e:
            logger.error(str(e))
            raise CustomException("Error during saving model and weights Process",e)
        

if __name__=="__main__":
    model_trainer = ModelTraining(PROCESSED_DIR)
    model_trainer.model_training()
    




        


