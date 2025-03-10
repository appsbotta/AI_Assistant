import os
import base64
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
        with open(os.path.join(save_dir,'repo.txt'),'w',encoding="utf-8") as f:
            logger.info(f"Starting writing data from git hub repos")
            for repo in repos:
                OWNER = repo['owner']['login']
                REPO = repo['name']
                readme = f"https://api.github.com/repos/{OWNER}/{REPO}/readme"
                headers = {"Authorization": f"token {os.getenv("TOKEN")}"}
                response = requests.get(readme, headers=headers)

                readme_content = "No Readme FIle"
                if response.status_code == 200:
                    data = response.json()
                    readme_content = base64.b64decode(data["content"]).decode()
                
                f.write(str(repo["name"]) + " -> " + str(repo["html_url"] +"\n"))
                f.write("Description \n")
                f.write(readme_content)
                f.write(str("\n"))
                f.write(str("\n"))
                f.write("<=================================================================================================>")
                f.write(str("\n"))
                f.write(str("\n"))
            logger.info(f"Completed writing data from git hub repos")