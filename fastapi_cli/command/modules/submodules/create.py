import typer
from rich.console import Console

from pathlib import Path
from typing_extensions import Annotated
from InquirerPy import inquirer

from fastapi_cli.utils.config.config import load_config, Module, save_config, Config, SubModule, Schema

app = typer.Typer()
console = Console()

def _get_module(config: Config) -> Module:
    module = None

    names_modules = config.get_name_of_modules()

    name_module: str = inquirer.select(
        message="Choose the Module :",
        choices=names_modules,
        default=names_modules[0],
    ).execute()

    module = config.get_module_by_name(name_module)
    return module

def _create_schema(config: Config, submodule: SubModule):

    name = Console.input("📝 what is the name of the schema :")
    name[0].upper()
    schema = Schema(name=name)
    file = f"""
from pydantic import BaseModel

class {schema.name}Base(BaseModel):
    pass
    
class {schema.name}In({schema.name}Base):
    pass
class {schema.name}Out({schema.name}Base):
    pass
"""

    schema.path = str(config.ProjectName + "/" + schema.path + "/" + str(schema.name) + ".py")

    filepath = Path(schema.path)

    if filepath.exists():
        console.print(f"💥 file not created: [cyan]{schema.path}[/cyan]")
        raise typer.Exit(code=1)
    filepath.write_text(file)
    submodule.schemas.append(schema)

    console.print(f"📝 Created file: [cyan]{schema.path}[/cyan]")

def _create_file(file_path: Path, submodule: SubModule, module: Module, config: Config):

    file_content_endpoint = f"""
from fastapi import APIRouter, status

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK, tags=["{module.name}:{submodule.name}"])
async def get_{submodule.name}():
    return""" + "{'data': 'the default page for the submodule'}"

    file_content_router = f"""
from api.{module.name}.endpoints import {submodule.name}
router_{module.name}.include_router({submodule.name}.router, prefix="/{submodule.name}", tags=["{module.name}:{submodule.name}"])

"""

    try:
        file_path.write_text(file_content_endpoint)
        console.print(f"📝 Created file: [cyan]{submodule.path}[/cyan]")

        name_path_module = Path(config.ProjectName + "/api/" + module.name + "/router.py")

        with name_path_module.open("a", encoding="utf-8") as f:
            f.write(file_content_router)

    except:
        console.print(f"💥 [red] Error pendant la création du router pour le module[/]")
        raise typer.Exit(code=1)


@app.command()
def create(
        name: Annotated[str, typer.Argument(help="Name of the SubModule")], 
        schema: Annotated[
            bool,
            typer.Option(
                help="Create schema for the submodule.", rich_help_panel="Customization and Utils"
            ),
        ] = False,
    ):
    """
    Create a new submodule
    """

    config = load_config()

    module = config.modules[0] if len(config.modules) == 1 else _get_module(config) 

    if not module:
        console.print(f"💥 [red] Error during the selection of Module[/]")
        raise typer.Exit(code=1)

    if module.is_submodule_exist(name.replace(" ", "_")):
        console.print(f"💥 [red] SubModule already exist [/]")
        raise typer.Exit(code=1)


    name_path = Path(config.ProjectName + "/api/" + module.name + "/endpoints/" + name.replace(" ", "_") + ".py")
    submodule = SubModule(name=name.replace(" ", "_"), path=str(name_path), schemas=[], services=[], routers=[])
    if schema:
        _create_schema(config, submodule)
    _create_file(name_path, submodule, module, config)
    module.submodules.append(submodule)
    save_config(config)
    console.print(f"💥 [green] submodule created with success ![/]")
