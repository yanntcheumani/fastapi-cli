from dataclasses import dataclass, asdict
from typing import List
import yaml
from pathlib import Path
from dacite import from_dict
from enum import StrEnum


NAME_CONFIG_FILE = ".fastapi-cli.yaml"


class HttpMethod(StrEnum):
    POST = "post"
    GET  = "get"
    PUT = "put"
    DELTE = "delete"

@dataclass
class BaseClass:
    path: str = ""
    name: str = ""

@dataclass
class Router:
    """
        Cette class permet de faire une route specifique pour management specifique sur un schema ou model (supprimer, récuperer, editer, etc)
    """
    method: HttpMethod | None
    schema: str | None
    path: str = ""
    name: str = ""


@dataclass
class Schema:
    inModule: bool = False
    path: str = "schemas"
    name: str = ""

@dataclass
class Service:
    path: str = ""
    name: str = ""



@dataclass
class SubModule:
    name: str | None

    routers: List[Router] | None
    schemas: List[Schema] | None
    services: List[Service] | None

@dataclass
class Module:
    submodules: List[SubModule] = None
    name: str = "v1"
    version: int = 1



@dataclass
class Config:
    modules: List[Module]
    schemas: List[Schema]
    services: List[Service]
    middlewares: List[BaseClass] | None = None
    ProjectName: str = "backend"
    isLoad: bool = False


    def get_name_of_modules(self):
        return [module.name for module in self.modules]
    

    def get_schemas(self) -> List[Schema]:
        list_schema = self.schemas.copy()

        for modules in self.modules:
            for submodule in modules.submodules:
                for schema in submodule.schemas:
                    list_schema.append(schema)

        return list_schema

    def get_name_of_schemas(self) -> List[str]:
        list_name_schema = [schema.name for schema in self.schemas] 

        for modules in self.modules:
            for submodule in modules.submodules:
                for schema in submodule.schemas:
                    list_name_schema.append(schema.name)

        return list_name_schema

    def get_schema(self, name: str) -> Schema:
        for schema in self.schemas:
            if schema.name == name:
                return schema

        for modules in self.modules:
            for submodule in modules.submodules:
                for schema in submodule.schemas:
                    if schema.name: return schema

        return None
    
    def delete_schema(self, schema: Schema):
        self.schemas = [s for s in self.schemas if s.name != schema.name]

        for modules in self.modules:
            for submodule in modules.submodules:
                for schema in submodule.schemas:
                    if schema.name == schema.name: 
                        submodule.schemas.remove(schema)

def load_config(config_path: Path = Path(NAME_CONFIG_FILE)) -> Config:
    if not config_path.exists():
        return Config(modules=[], schemas=[], services=[])
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return from_dict(data_class=Config, data=data)


def save_config(config: Config, config_path: Path = Path(NAME_CONFIG_FILE)):
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(asdict(config), f, sort_keys=False, allow_unicode=True)
