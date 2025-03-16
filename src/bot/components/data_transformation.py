import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from bot import logger
import json
import markdown2
import html2text
import base64
from pathlib import Path
from bot.entity.config_entity import DataTrasformationConfig
import shutil
from dotenv import load_dotenv
load_dotenv()

class DataTransformation:
    def __init__(self,config:DataTrasformationConfig):
        self.config = config

    def get_data(self):
        file_dir = self.config.file_dir
        for file_name in os.listdir(file_dir):
            if file_name.lower().endswith(".pdf"):  # Check if file is a PDF
                source_path = os.path.join(file_dir, file_name)
                destination_path = os.path.join(self.config.save_dir, file_name)
                shutil.copy2(source_path, destination_path)
    
        with open(os.path.join(file_dir,'data.json'),'r',encoding='utf-8') as f:
            data = json.load(f)
        
        return data
    
    def get_lang(self,repo_name):
        url = f'https://api.github.com/repos/appsbotta/{repo_name}/languages'
        headers = {"Authorization": f"token {os.getenv('TOKEN')}"}
        lang = requests.get(url,headers=headers).json()
        top_three_keys = sorted(lang, key=lang.get, reverse=True)[:3]
        # logger.info(f"Got top 3 languages used in {repo_name}")
        return top_three_keys
    
    def get_timings(self,repo):
        update = repo['updated_at'][:10]
        created = repo['created_at'][:10]
        pushed = repo['pushed_at'][:10]
        times = {
            "updated_at": update,
            "created_at":created,
            "pushed_at": pushed,
        }
        # logger.info(f"secured 3 timings {times.keys()}")
        return times
    
    def get_readme(self,OWNER,REPO):
        # logger.info(f"requeting readme file for the repo {REPO} ")
        readme = f"https://api.github.com/repos/{OWNER}/{REPO}/readme"
        headers = {"Authorization": f"token {os.getenv('TOKEN')}"}
        response = requests.get(readme,headers=headers)
        readme_content = "No Readme FIle"
        if response.status_code == 200:
            data = response.json()
            readme_content = base64.b64decode(data["content"]).decode("utf-8")
            readme_content =  markdown2.markdown(readme_content, extras=["strip"])
            readme_content = html2text.html2text(readme_content)
        # logger.info(f"Request for README file for the repo {REPO} completed")
        return readme_content
    
    
    def get_pdf_from_data(self):
        logger.info("Saving data to a pdf file started")
        save_dir = self.config.save_dir
        data = self.get_data()

        doc = SimpleDocTemplate(os.path.join(save_dir,'repo.pdf'), pagesize=letter)
        styles = getSampleStyleSheet()
        custom_style = ParagraphStyle(
            'Custom',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=10,
            leading=14,  # Line height
            spaceAfter=5,
        )
        heading_style = ParagraphStyle(
            "HeadingStyle",
            parent=styles["Heading1"],
            fontName="Courier-Bold",
            fontSize=16,
            leading=22,

        )

        content = []



        for i,repo in enumerate(data):
            text = f"{i+1}. <b>{repo['name']}</b>  --->   {repo['html_url']} \n"
            # text = text + str(i+1) + ". " +  str(repo["name"]) + " -> " + str(repo["html_url"]) +"\n"
            paragraph = Paragraph(text,custom_style)
            content.append(paragraph)
        content.append(Spacer(1,5))
        
        for i,repo in enumerate(data):
            OWNER = repo['owner']['login']
            REPO = repo['name']
            readme = self.get_readme(OWNER,REPO)
            timings = self.get_timings(repo)
            lang = self.get_lang(REPO)
            heading = Paragraph(f"{i+1}. {REPO}",heading_style)
            content.append(heading)
            for key,value in timings.items():
                text = f"{key} -> {value}"
                paragraph = Paragraph(text,custom_style)
                content.append(paragraph)
            lang_text = "   "
            for it in lang:
                lang_text = lang_text + it +", "
            text = Paragraph(lang_text,custom_style)
            content.append(text)
            readme = Preformatted(readme,custom_style)
            content.append(readme)
            content.append(Spacer(1, 5))


        doc.build(content)
        logger.info("saving data to a pdf file is completed")
    
    
        
    

    
        