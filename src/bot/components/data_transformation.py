import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from bot import logger
from pathlib import Path
from bot.entity.config_entity import DataTrasformationConfig

class DataTransformation:
    def __init__(self,config:DataTrasformationConfig):
        self.config = config
    
    def get_pdf_from_text(self):
        save_dir = self.config.save_dir
        file_path = Path(self.config.file_dir)
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

        content = []
        logger.info("Starting the process of converting text to pdf")
        with open(os.path.join(file_path,'repo.txt'), "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if line.strip() == "<=================================================================================================>":
                    paragraph = Preformatted(line.strip(), custom_style)
                else:
                    paragraph = Paragraph(line.strip(), custom_style)     # Wrap text automatically
                content.append(paragraph)
                content.append(Spacer(1, 5))  # Preserve spacing
        
        doc.build(content)

        logger.info("Completed converting text to pdf")
    

    
        