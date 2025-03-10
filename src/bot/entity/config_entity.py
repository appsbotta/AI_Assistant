from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    github_url: str
    save_dir: Path

@dataclass(frozen=True)
class DataTrasformationConfig:
    root_dir: Path
    file_dir: Path
    save_dir: Path