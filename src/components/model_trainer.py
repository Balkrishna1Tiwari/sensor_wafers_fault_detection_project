import sys

from src.utils.main_utils import MainUtils
import sys
import warnings
warnings.filterwarnings('ignore')
from dataclasses import dataclass
from typing import Generator, List, Tuple
import os
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC

from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier

from xgboost import XGBClassifier

from sklearn.model_selection import GridSearchCV,train_test_split
from src.exception import CustomException
from src.logg import logging
@dataclass
class ModelConfiguration:
    
    model_path=os.path.join('artifacts','model.pkl')
    
    yml=r"C:\Users\balkr\big_project\confi_yaml\model.yaml"
    
class Model_Trainer:
    
    def __init__(self):
        
        self.model_path_file=ModelConfiguration()
        self.utils = MainUtils()
        self.model={
            
            
            
            
             'XGBClassifier': XGBClassifier(),
                        'GradientBoostingClassifier' : GradientBoostingClassifier(),
                        'SVC' : SVC(),
                        'RandomForestClassifier': RandomForestClassifier()
                        
               
        }
        
       
    def evaluate_model(self,x_train,y_train,x_test,y_test,models):
        try:
        
            report={}


            for i in range(len(models)):
            
                model=list(models.values())[i]
            
                model.fit(x_train,y_train)
            
                pred=model.predict(x_test)
            
                acc=accuracy_score(y_test,pred)
            
                report[list(models.keys())[i]]=acc
            
            return report
        
        except Exception as e:
            raise CustomException(str(e),sys)
        
        
        
        
    def get_best_model(self, x_train, y_train, x_test, y_test, models):
        
        try:
            
            
            model_report = self.evaluate_model(x_train, y_train, x_test, y_test, models)
    
       
            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]


            best_model = models[best_model_name]

    
            return best_model_name, best_model, best_model_score
        
        except Exception as e:
            
            raise CustomException(str(e),sys)
        
        
        
        
    def fine_tune_model(self, model_name,model_object, x_train, y_train, x_test, y_test):
        # model_class_name = type(model_object).__name__
        # print(model_class_name)
        
        try:
            param = self.utils.read_yaml_file(self.model_path_file.yml)["model_selection"]["model"][model_name]["search_param_grid"]
            print(param)
            model = GridSearchCV(estimator=model_object, param_grid=param, cv=2, n_jobs=-1, verbose=1)
        
            return model
        
        
        except Exception as e:
            
            raise CustomException(str(e),sys)

    
    def initiate_model_trainer(self, x_train, y_train, x_test, y_test):
        
        
        logging.info(f"Splitting training and testing input and target feature")
        
        
        try:
            
            x_train = pd.read_csv(x_train)
            x_train = x_train.drop('Unnamed: 0', axis=1)
            y_train = pd.read_csv(y_train)
            y_train = y_train.drop('Unnamed: 0', axis=1)
            y_train = y_train  # Convert y_train to a 1D array

            x_test = pd.read_csv(x_test)
            x_test = x_test.drop('Unnamed: 0', axis=1)
            y_test = pd.read_csv(y_test)
            y_test = y_test.drop('Unnamed: 0', axis=1)
            y_test = y_test  # Convert y_test to a 1D array

            best_model_name, best_model_object, best_model_score = self.get_best_model(x_train, y_train, x_test, y_test, self.model)
            best_model = self.fine_tune_model(best_model_name,best_model_object, x_train, y_train, x_test, y_test)

            best_model.fit(x_train, y_train)
            pred = best_model.predict(x_test)

            score = accuracy_score(y_test, pred)

            print(f"best model name {best_model_name} and score: {best_model_score}")
            
            if best_model_score < 0.5:
                raise Exception("No best model found with an accuracy greater than the threshold 0.6")
            
            logging.info(f"Best found model on both training and testing dataset")
            
            logging.info(
                f"Saving model at path: {self.model_path_file.model_path}"
            )


            self.utils.save_object(self.model_path_file.model_path, best_model)

            return self.model_path_file.model_path
        
        except Exception as e:
            raise CustomException(str(e),sys)
    
# v




