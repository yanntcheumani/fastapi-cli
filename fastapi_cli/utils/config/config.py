from dataclasses import dataclass, asdict
from typing import List
import yaml
from pathlib import Path


from fastapi_cli.utils.globals import NAME_CONFIG_FILE


@dataclass
class BaseClass:
    path: Path = Path("")
    name: str = ""

@dataclass
class Router(BaseClass):
    pass

@dataclass
class Schema(BaseClass):
    pass

@dataclass
class Service(BaseClass):
    pass


@dataclass
class Module:
    router: Router
    schemas: Schema
    service: Service
    crud: BaseClass
    middlewares: BaseClass
    name: str = ""



@dataclass
class Config:
    modules: List[Module]
    schemas: List[Schema]
    service: List[Service]
    ProjectName: str = "backend"



def load_config(config_path: Path = Path(NAME_CONFIG_FILE)) -> Config:
    if not config_path.exists():
        return Config()
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return Config(**data)

def save_config(config: Config, config_path: Path = Path(NAME_CONFIG_FILE)):
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(asdict(config), f, sort_keys=False, allow_unicode=True)