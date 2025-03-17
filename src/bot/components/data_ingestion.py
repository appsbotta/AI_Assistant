import os
import requests
import zipfile
from urllib import request
import json
from bot import logger
from dotenv import load_dotenv
load_dotenv()
from bot.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self,config:DataIngestionConfig):
        self.config = config
    
    def get_repos(self):
        logger.info(f"Starting writing data from git hub repos")
        url = self.config.github_url
        headers = {"Authorization": f'token {os.getenv("TOKEN")}'}
        repos = requests.get(url, headers=headers).json()
        save_dir = self.config.save_dir
        with open(os.path.join(save_dir,"data.json"),'w',encoding='utf-8') as f:
            json.dump(repos,f,indent=4)
        logger.info(f"Completed writing data from git hub repos")

    def downloadFiles(self):
        if not os.path.exists(self.config.local_data_file):
            filename , headers = request.urlretrieve(
                url = self.config.linkedin_url,
                filename = self.config.local_data_file
            )
            logger.info(f"{filename} download! with following info: \n{headers}")
        else:
            logger.info(f"file already exists of size")
    
    def extractZip(self):
        unzip_path = self.config.save_dir
        os.makedirs(unzip_path,exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file,'r') as zip_ref:
            zip_ref.extractall(unzip_path)