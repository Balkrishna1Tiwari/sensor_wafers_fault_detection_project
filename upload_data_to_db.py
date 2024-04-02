from pymongo.mongo_client import MongoClient
import pandas as pd
import json

# uniform resource indentifier


# Create a new client and connect to the server
client = MongoClient(uri)

# create database name and collection name
MONGO_DB_URL='mongodb+srv://balkrishnatiwari389:balkrishnatiwari389@cluster0.yc3cqg5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'


# AWS_S3_BUCKET_NAME = "wafer-fault"
MONGO_DATABASE_NAME = "wafers_sensor_data"
MONGO_COLLECTION_NAME = "my_data"
df=pd.read_csv(r"C:\Users\balkr\big_project\artifacts\raw.csv")
df=df.drop("Unnamed: 0",axis=1)

# Convert the data into json
json_record=list(json.loads(df.T.to_json()).values())

#now dump the data into the database
client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)

df=df.drop("Unnamed: 0",axis=1)

# Convert the data into json
json_record=list(json.loads(df.T.to_json()).values())

#now dump the data into the database
client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
