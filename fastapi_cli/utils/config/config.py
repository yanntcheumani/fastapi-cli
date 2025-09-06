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
    method: str | None
    schema: str | None
    path: str = ""
    router_name: str = ""
    url_name: str = ""

@dataclass
class Schema:
    inModule: bool = False
    path: str = "schemas"
    name: str = ""

    def __repr__(self):
        return f"<Schema(name={self.name}, path={self.path}, inModule={self.inModule})"

@dataclass
class Service:
    path: str = ""
    name: str = ""




@dataclass
class SubModule:
    name: str | None
    path: str | None
    routers: List[Router] | None
    schemas: List[Schema] | None
    services: List[Service] | None
    name_module: str | None

    def get_name_of_routers(self) -> List[str]:
        list_name_router = [router.name for router in self.routers] 

        return list_name_router

    def get_router_by_name(self, name: str) -> Router:
        for router in self.routers:
            if router.router_name == name:
                return router
        return None

    def get_name_of_schemas(self) -> List[str]:
        return [schema.name for schema in self.schemas]
    
    def is_router_exist(self, method_name, url_name) -> bool:
        
        for router in self.routers:
            if router.method == method_name and router.url_name == url_name:
                return True
        return False


@dataclass
class Module:
    submodules: List[SubModule] = None
    name: str = "v1"
    version: int = 1

    def is_submodule_exist(self, name: str) -> bool:
        for submodule in self.submodules:
            if submodule.name == name: return True
        return False
    
    def get_submodule_by_name(self, name: str) -> SubModule:
        for submodule in self.submodules:
            if submodule.name == name: return submodule
        return submodule



@dataclass
class Config:
    modules: List[Module]
    schemas: List[Schema]
    services: List[Service]
    middlewares: List[BaseClass] | None = None
    ProjectName: str = "backend"
    isLoad: bool = False

    def get_submodule_by_name(self, name: str) -> SubModule:
        for module in self.modules:
            submodule = module.get_submodule_by_name(name)
            if submodule: return submodule
        return None
 
    def get_name_of_modules(self):
        return [module.name for module in self.modules]
    
    def get_module_by_name(self, name: str) -> Module:
        for module in self.modules:
            if module.name == name: return module

        return None

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
                    if schema.name == name: return schema

        return None
    
    def get_name_with_one_submodule(self, submodule: SubModule) -> List[str]:
        list_name_schema = [schema.name for schema in self.schemas] 
        
        return list_name_schema + submodule.get_name_of_schemas()

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
