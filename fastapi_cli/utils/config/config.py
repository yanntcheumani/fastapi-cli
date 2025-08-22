from dataclasses import dataclass, asdict
from typing import List
import yaml
from pathlib import Path



NAME_CONFIG_FILE = ".fastapi-cli.yaml"

@dataclass
class BaseClass:
    path: str = ""
    name: str = ""

@dataclass
class Router(BaseClass):
    pass

@dataclass
class Schema(BaseClass):
    path: str = "schemas"
    pass

@dataclass
class Service(BaseClass):
    pass


@dataclass
class Module:
    router: Router
    schema: Schema
    service: Service
    crud: BaseClass
    middlewares: BaseClass
    name: str = ""



@dataclass
class Config:
    modules: List[Module]
    schemas: List[Schema]
    services: List[Service]
    ProjectName: str = "backend"
    isLoad: bool = False

def load_config(config_path: Path = Path(NAME_CONFIG_FILE)) -> Config:
    if not config_path.exists():
        return Config(modules=[], schemas=[], services=[])
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return Config(**data)

def save_config(config: Config, config_path: Path = Path(NAME_CONFIG_FILE)):
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(asdict(config), f, sort_keys=False, allow_unicode=True)