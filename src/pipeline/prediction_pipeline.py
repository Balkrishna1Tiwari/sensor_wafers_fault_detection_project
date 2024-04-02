
import shutil
import os,sys
import pandas as pd
import pickle

import sys
from flask import request

from src.utils.main_utils import MainUtils

from dataclasses import dataclass
        
from src.exception import CustomException
from src.logg import logging


import os

from dataclasses import dataclass

from src.utils.main_utils import MainUtils


@dataclass

class Prediction_pipeline_Config:
    prediction_output_dirname: str = "predictions"
    prediction_file_name:str =  "predicted_file.csv"
    model_file_path: str = os.path.join('artifacts', "model.pkl" )
    preprocessor_path: str = os.path.join('artifacts', "preprocessor.pkl")
    prediction_file_path:str = os.path.join(prediction_output_dirname,prediction_file_name)

class PredictionPipeline:
    
    def __init__(self,request: request):
        
        self.pred_config=Prediction_pipeline_Config()
        self.utils=MainUtils()
        
        self.request=request
        
    def save_input_file(self):
        
        try:
            pred_file_input_dir = "prediction_artifacts"
            os.makedirs(pred_file_input_dir, exist_ok=True)
            input_file=self.request.files['file']
        
       
            pred_file_path = os.path.join(pred_file_input_dir, input_file.filename)
            
        
            input_file.save(pred_file_path)
            
            return pred_file_path
        
        
        except Exception as e:
            raise CustomException(str(e),sys)
        
        
        
        
    def predict(self,input_data):
        try:
            
            model=self.utils.load_object(self.pred_config.model_file_path)
        
            preprocessor=self.utils.load_object(self.pred_config.preprocessor_path)
        
            scaled=preprocessor.transform(input_data)
        
            data=model.predict(scaled)
        
            return data
        
        except Exception as e:
            raise CustomException(str(e),sys)
        
        
        
        
    def get_data_as_data_frame(self,file_path):
        try:
            
            prediction_column_name : str = 'TARGET_COLUMN'
            input_data_frame=pd.read_csv(file_path)
        
            input_data_frame=input_data_frame.drop("Unnamed: 0",axis=1) if "Unnamed: 0" in input_data_frame.columns else input_data_frame
            
            predictions=self.predict(input_data_frame)
            
            input_data_frame[prediction_column_name] = [pred for pred in predictions]
            
            target_column_mapping = {0:'bad', 1:'good'}

            os.makedirs(self.pred_config.prediction_output_dirname,exist_ok=True)
        
            input_data_frame[prediction_column_name] = input_data_frame[prediction_column_name].map(target_column_mapping)
            
            input_data_frame.to_csv(self.pred_config.prediction_file_path,index=False)
            
            logging.info("predictions completed. ")
            
            return input_data_frame
        
        
        except Exception as e:
            raise CustomException(str(e),sys)
        
        
        
        
    def run_pipeline(self):
        
        try:
            input_csv_path = self.save_input_file()
            self.get_data_as_data_frame(input_csv_path)

            return self.pred_config

        except Exception as e:
            
            raise CustomException(str(e),sys)
        
        
        
        
    
    
    
    