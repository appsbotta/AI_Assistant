import os
import requests
from bot import logger
from dotenv import load_dotenv
load_dotenv()
from bot.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self,config:DataIngestionConfig):
        self.config = config
    
    def get_repos(self):
        url = self.config.github_url
        headers = {"Authorization": f"token {os.getenv("TOKEN")}"}
        repos = requests.get(url, headers=headers).json()
        save_dir = self.config.save_dir
        with open(os.path.join(save_dir,'repo.txt'),'a') as f:
            for repo in repos:
                f.write(str(repo["name"]) + " -> " + str(repo["html_url"] + "\n"))