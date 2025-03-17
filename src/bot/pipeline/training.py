from bot import logger
from bot.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from bot.pipeline.stage_02_data_transformation import DataTransformationTrainingPipeline

class TrainingPipeline:
    def __init__(self):
        pass

    def train(self):
        STAGE_NAME = "Data Ingestion stage"
        try:
            logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
            data_ingestion = DataIngestionTrainingPipeline()
            data_ingestion.main()
            logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        except Exception as e:
            logger.exception(e)
            raise e

        STAGE_NAME = "Data Transformation stage"
        try:
            logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
            data_transformation = DataTransformationTrainingPipeline()
            data_transformation.main()
            logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        except Exception as e:
            logger.exception(e)
            raise e