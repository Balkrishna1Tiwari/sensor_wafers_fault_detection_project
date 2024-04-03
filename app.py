from flask import Flask, render_template, jsonify, request, send_file

import os
import sys
from src.exception import CustomException
sys.path.append(r"C:\Users\balkr\big_project\src\pipeline")
from training_pipeline import TrainingPipeline
from prediction_pipeline import PredictionPipeline
from src.logg import logging
app=Flask(__name__)

@app.route('/train')

def train_route():
    
    train=TrainingPipeline()
    
    train.run_pipeline()
    return 'training completed'

@app.route('/predict',methods=['GET','POST'])

def upload():
    try:
        if request.method=='POST':
            
            predictpipeline=PredictionPipeline(request)
            prediction_file_detail=predictpipeline.run_pipeline()
            
            logging.info("prediction completed. Downloading prediction file.")
            
            return send_file(prediction_file_detail.prediction_file_path,
                            download_name= prediction_file_detail.prediction_file_name,
                            as_attachment= True)
        else:
        
            return render_template('upload_file.html')
        
        
    except Exception as e:
        raise CustomException(str(e),sys)
    
#exicution will start here
    
if __name__=="__main__":

    app.run(host="0.0.0.0", port=5000, debug= True)