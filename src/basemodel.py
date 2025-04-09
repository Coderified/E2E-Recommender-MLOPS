from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dot, Dense, Flatten,Activation,BatchNormalization
from utils.common_functions import read_yaml
from src.logger import get_logger
from src.custom_exception import CustomException
from tensorflow.keras import backend as K
import tensorflow as tf
print(tf.__version__)

logger = get_logger(__name__)

class BaseModel:
    def __init__(self, config_path):
        try:
            self.config = read_yaml(config_path)
            logger.info("Loaded config file from config.yaml")
        except Exception as e:
            raise CustomException("Error loading config file", e)
        
    def RecommenderNet(self, n_users, n_anime):
        try:
            print(tf.__version__)
            logger.info("Creating the model")
            embedding_size = self.config['model']['embedding_dim']

            logger.info("User input and embedding layer to begin")  
            user = Input(shape=[1], name='user')
            
            logger.info("User Embedding layer to begin") 
            user_embedding = Embedding(input_dim=n_users, output_dim=embedding_size, name='user_embedding')(user)
            # means the whole embedding layer will be working on this input layer 

            logger.info("Anime input and embedding layer to begin")  
            anime = Input(shape=[1], name='anime')
            anime_embedding = Embedding(input_dim=n_anime, output_dim=embedding_size, name='anime_embedding')(anime)

            #Dot layer to calculate the dot product of user and anime embeddings
            #Dot product is a measure of similarity between two vectors 
            logger.info("Dot product to begin")
            print("User embedding shape:", K.int_shape(user_embedding))
            print("Anime embedding shape:", K.int_shape(anime_embedding))
            x = Dot(name="Dot_Product", normalize=True, axes=2)([user_embedding, anime_embedding])

            #x = Flatten()(x) #Flattening the output of dot product layer to convert it into a 1D vector
            #Dot product layer output is a 3D tensor, so we need to flatten it to 2D tensor
            logger.info("Flatten to begin")
            x = Flatten()(x)

            logger.info("Dense to begin")
            x= Dense(1,kernel_initializer='he_normal')(x) #Dense layer to convert the 2D tensor to a single value

            logger.info("Batch Norm to begin")
            x = BatchNormalization()(x) #Batch normalization to normalize the output of the dense layer

            logger.info("Acitvation to begin")
            x = Activation("sigmoid")(x) #Activation function to convert the output to a value between 0 and 1


            model = Model(inputs=[user,anime],outputs = x) #Creating the model with user and anime as inputs and x as output

        #Compiling the model with binary crossentropy loss and adam optimizer
            logger.info("Model compilation to begin")
            model.compile(loss=self.config['model']['loss_function'], 
                          optimizer=self.config['model']['optimizer'], 
                          metrics=self.config['model']['metrics']) 
            
            logger.info("Model compiled successfully")
            logger.info(f"Model summary: {model.summary()}")

            return model
        except Exception as e:
            logger.error("Error in creating the model")
            raise CustomException("Error in creating the model", e)