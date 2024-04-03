import os 
import pickle
import yaml
from src.exception import CustomException
import sys
from src.logg import logging
class MainUtils:
    
    
    
    def __init__(self) -> None:
        pass

    def read_yaml_file(self, filename: str) -> dict:
        try:
            
            
            with open(filename, "rb") as yaml_file:
                return yaml.safe_load(yaml_file)
            
            
        except Exception as e:
            raise CustomException(str(e),sys)
       


    def save_object(self,file_path: str, obj):
        
        try:
            
            
            with open(file_path, 'wb') as fil_obj:
                pickle.dump(obj, fil_obj)
                
        except Exception as e:
            raise CustomException(str(e),sys)
            

    @staticmethod
    def load_object(file_path: str) -> object:
        
        try:
            
            with open(file_path, "rb") as file_obj:
                obj = pickle.load(file_obj)
        
            # logging.info("Exited the load_object method of MainUtils class")

            return obj
        
        except Exception as e:
            raise CustomException(str(e),sys)
    

        