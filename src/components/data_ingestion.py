import pandas as pd
import os
import sys
from pymongo import *
sys.path.append(r'C:\Users\balkr\big_project\src\pipeline\constant')
from db_info import*
import sys
import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from zipfile import Path
# from src.utils import main_utils
from src.exception import CustomException
from src.logg import logging
from dataclasses import dataclass

@dataclass

class DataIngestionConfig:
    dir_path='artifacts'
    filepath=os.path.join('artifacts','raw.csv')
    
    
class DataIngestion:
    
    def __init__(self):
        
        self.data_ingestion_config=DataIngestionConfig()
        
        # self.utils=main_utils()
        
    def get_exported_as_data_frame(self,db_name,coll_name):
        try:
            
            mongo_client = MongoClient(MONGO_DB_URL)

            collection = mongo_client[db_name][coll_name]
        
            df = pd.DataFrame(list(collection.find()))
            print(df)
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
                
            df.replace({"na": np.nan}, inplace=True)
           
            return df
        
        except Exception as e:
            
             
            raise CustomException(e, sys)
    def store_in_file_path(self):
        
        try:
            
            
            os.makedirs(self.data_ingestion_config.dir_path,exist_ok=True)
            
            logging.info(f"Exporting data from mongodb")
            
            data=self.get_exported_as_data_frame(MONGO_DATABASE_NAME,MONGO_COLLECTION_NAME)
            
            file_path=(self.data_ingestion_config.filepath)
            
            data.to_csv(self.data_ingestion_config.filepath,index=False)
           
            logging.info(f"Saving exported data into feature store file path: {file_path}")
            
            return file_path
        
        except Exception as e:
            raise CustomException(e, sys)
        
        
    def initiate_data_ingestion(self):
       
        file_path=self.store_in_file_path()
        
        return file_path
       

