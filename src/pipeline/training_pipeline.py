import sys,os
sys.path.append(r'C:\Users\balkr\big_project\src\components')
from data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import Model_Trainer

from src.exception import CustomException
from src.logg import logging






class TrainingPipeline:
    
    def __init__(self):
        pass
    
    def start_data_ingestion(self):
        
        try:
            self.data_ingestion=DataIngestion()
        
            path_of_data=self.data_ingestion.initiate_data_ingestion()
        
            return path_of_data
        
        except Exception as e:
            raise CustomException(str(e),sys)
        
        
    def start_data_trandformation(self,path):
        
        try:
        
            self.data_transform=DataTransformation()
        
            x_train,y_train,x_test,y_test,preprocessor=self.data_transform.initiate_data_transformation(path)
        
            return  x_train,y_train,x_test,y_test,preprocessor
        
        
        except Exception as e:
            raise CustomException(str(e),sys)
        
        
        
    def start_model_training(self,x_train,y_train,x_test,y_test):
        
        try:
            
            self.model_training=Model_Trainer()
            self.model_training.initiate_model_trainer(x_train,y_train,x_test,y_test)
        
        
        except Exception as e:
            
            raise CustomException(str(e),sys)
        
        
        
        
    def run_pipeline(self):
        
        try:
        
            path=self.start_data_ingestion()
           
            x_train,y_train,x_test,y_test,preprocessor=self.start_data_trandformation(path)
        
            self.start_model_training(x_train,y_train,x_test,y_test)
           
        except Exception as e:
            
            
            raise CustomException(str(e),sys)
