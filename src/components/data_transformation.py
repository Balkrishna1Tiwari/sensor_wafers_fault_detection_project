from dataclasses import dataclass
import sys

from  src.utils.main_utils import MainUtils
import sys
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from src.exception import CustomException
from src.logg import logging


@dataclass
class DataTransformation_config:
    
    dir_name='artifacts'
    path=os.path.join(dir_name,'preprocessor.pkl')
    save_x_train=os.path.join(dir_name,'x_train.csv')
    save_y_train=os.path.join(dir_name,'y_train.csv')
    save_x_test=os.path.join(dir_name,'x_test.csv')
    save_y_test=os.path.join(dir_name,'y_test.csv')
    
class DataTransformation:
    
    def __init__(self):
        
        self.config=DataTransformation_config()
        
        self.utils=MainUtils()
        
    def get_data_transformation_object(self):
        
        try:
        
            imputer=('simple',SimpleImputer(strategy='constant',fill_value=0))
            scaler=('robust',RobustScaler())
        
            preprocesser=Pipeline(steps=[imputer,
                                         
                                     scaler]
                              )
        
            return preprocesser
        
        except Exception as e:
            raise CustomException(str(e),sys)
        
        
    def initiate_data_transformation(self,data_path):
        try:
            
            logging.info(
            "Entered initiate_data_transformation method of Data_Transformation class"
        )

            os.makedirs(self.config.dir_name,exist_ok=True)
        
            data=pd.read_csv(data_path)
            
            data=data.drop("Unnamed: 0",axis=1)
            
            data['Good/Bad']= np.where(data['Good/Bad']==-1,0,1)
        
            ind=data.iloc[:,:-1]
            dep=data.iloc[:,-1]
            
        # print(dep)
        # dep =np.where(dep[1]==-1,0, 1)
            X_train,X_test,y_train,y_test=train_test_split(ind,dep,test_size=0.20)
        
            preprocessor_obj=self.get_data_transformation_object()
        
        
        
            X_train1=preprocessor_obj.fit_transform(X_train)
            X_test1=preprocessor_obj.transform(X_test)
            
            
            
            X_train_df = pd.DataFrame(X_train1, columns=X_train.columns)
            X_test_df = pd.DataFrame(X_test1, columns=X_test.columns)
            
            
            
            X_train_df.to_csv(self.config.save_x_train)
            y_train.to_csv(self.config.save_y_train)
            X_test_df.to_csv(self.config.save_x_test)
            y_test.to_csv(self.config.save_y_test)
            
            
            
       
            self.utils.save_object(self.config.path,preprocessor_obj)
            
        
            return self.config.save_x_train,self.config.save_y_train,self.config.save_x_test,self.config.save_y_test,self.config.path
        
        except Exception as e:
            raise CustomException(str(e),sys)
# d=DataTransformation()        
# d.initiate_data_transformation(r'C:\Users\balkr\big_project\artifacts\raw.csv')      
        
        
        
         
        
    
    
# # C:\Users\balkr\big_project\artifacts\raw.csv