from dataclasses import dataclass, asdict
from typing import List
import yaml
from pathlib import Path
from dacite import from_dict



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
    inModule: bool = False
    pass

@dataclass
class Service(BaseClass):
    pass


@dataclass
class Module:
    router: Router | None
    schema: Schema | None
    service: Service | None
    crud: BaseClass | None
    middlewares: BaseClass | None
    name: str = ""



@dataclass
class Config:
    modules: List[Module]
    schemas: List[Schema]
    services: List[Service]
    ProjectName: str = "backend"
    isLoad: bool = False

    def get_schemas(self) -> List[Schema]:
        return self.schemas.copy() + [module.schema for module in self.modules if module.schema]
    

    def get_name_of_schemas(self) -> List[str]:
        return [schema.name for schema in self.schemas] + [module.schema.name for module in self.modules if module.schema]

    def get_schema(self, name: str) -> Schema:
        for schema in self.schemas:
            if schema.name == name:
                return schema
        
        for module in self.modules:
            if not module.schema:
                continue

            if module.schema.name == name:
                return module.schema

        return None
    
    def delete_schema(self, schema: Schema):
        self.schemas = [s for s in self.schemas if s.name != schema.name]

        for module in self.modules:
            if module.schema and module.schema.name == schema.name:
                module.schema = None


def load_config(config_path: Path = Path(NAME_CONFIG_FILE)) -> Config:
    if not config_path.exists():
        return Config(modules=[], schemas=[], services=[])
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return from_dict(data_class=Config, data=data)


def save_config(config: Config, config_path: Path = Path(NAME_CONFIG_FILE)):
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(asdict(config), f, sort_keys=False, allow_unicode=True)
