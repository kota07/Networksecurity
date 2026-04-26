import os
import json
import sys
import pandas as pd
import numpy as np
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


# Load environment variables from .env file
load_dotenv()
# Get MongoDB URL from environment variable
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)


import certifi
ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def cv_to_json_converter(self, file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(inplace=True)
            records=list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_mongodb(self, records,database, collection):

        try:
            self.records = records
            self.database = database
            self.collection = collection

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    FILE_PATH  = r"E:\NETWORKSECURITY\Network_data\phisingData.csv"
    database = "NetworkSecurity"
    collection = "PhishingData" 
    network_obj = NetworkDataExtract()
    records = network_obj.cv_to_json_converter(FILE_PATH)
    print(records)
    no_of_records = network_obj.insert_data_mongodb(records, database, collection)
    print(f"{no_of_records} records inserted successfully into MongoDB.")





