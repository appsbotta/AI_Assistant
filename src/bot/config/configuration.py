from bot.constants import *
from bot.utils.common import read_yaml,create_directories
from bot.entity.config_entity import (
    DataIngestionConfig,
)

class ConfigurationManager:
    def __init__(
            self,
            config_path = CONFIG_PATH,
            params_path = PARAMS_PATH
        ):
        self.config = read_yaml(config_path)
        self.param = read_yaml(params_path)

        create_directories([self.config.artifacts_root])
    
    def get_data_ingestion_config(self)->DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            github_url=config.github_url,
            save_dir=config.save_dir
        )

        return data_ingestion_config