import typer
from rich.console import Console
from rich.prompt import Prompt
from pathlib import Path
from typing_extensions import Annotated
from InquirerPy import inquirer
from typing import List

from fastapi_cli.command.modules.submodules.utils.create_router import create_router_content
from fastapi_cli.utils.config.config import load_config, Module, save_config, Config, SubModule, Schema, Router
from fastapi_cli.command.modules.submodules.utils.delete_router import delete_router_content

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

def _create_schema(config: Config, submodule: SubModule, schema_name: str = None):

    if not schema_name:
        schema_name = Prompt.ask(f"📝 what is the name of the schema")
        schema_name[0].upper()
    schema = Schema(name=schema_name)
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
    submodule = SubModule(name=name.replace(" ", "_"), path=str(name_path), schemas=[], services=[], routers=[], name_module=module.name)

    if schema:
        _create_schema(config, submodule)

    _create_file(name_path, submodule, module, config)
    module.submodules.append(submodule)
    save_config(config)
    console.print(f"💥 [green] submodule created with success ![/]")


@app.command()
def create_schema(
    name_submodule: Annotated[str, typer.Argument(help="Name of the SubModule")],
    name_schema: Annotated[str, typer.Argument(help="Name of the schema")], 
):
    """
    this command create schema in the submodule
    """

    config = load_config()

    if config.get_schema(name_schema):
        console.print(f"💥 [red] {name_schema} Schema already exist ! [/]")
        raise typer.Exit(code=1)

    submodule: SubModule = config.get_submodule_by_name(name_submodule)

    _create_schema(config, submodule, name_schema)
    save_config(config)

def _get_schema_in(config: Config, submodule: SubModule) -> str:
    names_schemas = config.get_name_with_one_submodule(submodule) + ["None", "List"]
    name_schema_in = inquirer.select(
            message="Choose the schema entry for this router :",
            choices=names_schemas,
            default=names_schemas[0],
        ).execute()
    
    if name_schema_in == "None":
        return name_schema_in
    
    if name_schema_in == "List":
        tmp_schemas = config.get_name_with_one_submodule(submodule)
        tmp_schema = inquirer.select(
            message="Choose the schema entry for this router :",
            choices=tmp_schemas,
            default=tmp_schemas[0],
        ).execute()
        name_schema_in = name_schema_in + "[" + tmp_schema + "In]"

        return name_schema_in
    return name_schema_in + "IN"

def _get_schema_out(config: Config, submodule: SubModule) -> str:
    names_schemas = config.get_name_with_one_submodule(submodule) + ["None", "List"]
    name_schema_out = inquirer.select(
            message="Choose the schema response for this router :",
            choices=names_schemas,
            default=names_schemas[0],
        ).execute()
    
    if name_schema_out == "None":
        return name_schema_out
    
    if name_schema_out == "List":
        tmp_schemas = config.get_name_with_one_submodule(submodule)
        tmp_schema = inquirer.select(
            message="Choose the schema response for this router :",
            choices=tmp_schemas,
            default=tmp_schemas[0],
        ).execute()
        name_schema_out = name_schema_out + "[" + tmp_schema + "Out]"

        return name_schema_out
    
    return name_schema_out + "Out"


@app.command()
def create_router(
    name_submodule: Annotated[str, typer.Argument(help="Name of the SubModule")],
    name_router: Annotated[str, typer.Argument(help="Name of the router")], 
):
    config = load_config()
    all_method = ["post", "get", "put", "delete"]

    submodule: SubModule = config.get_submodule_by_name(name_submodule)

    if submodule.get_router_by_name(name_router):
        console.print(f"💥 [red] {name_router} router already exist ! [/]")
        raise typer.Exit(code=1)

    name_method: str = inquirer.select(
        message="Choose the type of your router :",
        choices=all_method,
        default=all_method[0],
    ).execute()
    name_url = Prompt.ask(f"📝 what is the name of the url (by default it will be '/')", default="")
    name_schema_out = _get_schema_out(config, submodule)
    name_schema_in = _get_schema_in(config, submodule)

    if submodule.is_router_exist(name_method, name_url):
        console.print(f"💥 [red] the url: {name_url} with the method {name_method} already exist ![/]")
        raise typer.Exit(code=1)

    create_router_content(config, name_method, name_router, name_url, name_schema_out, name_schema_in, submodule)
    
    
    router = Router(method=name_method, schema=name_schema_out, router_name=name_router, url_name=name_url)
    submodule.routers.append(router)

    save_config(config)
    console.print(
        f"[bold green]📡 Router[/bold green] [cyan]{name_router}[/cyan] "
        f"a bien été ajouté au submodule [magenta]{submodule.name}[/magenta] 🎉"
    )

@app.command()
def delete_router(
    name_submodule: Annotated[str, typer.Argument(help="Name of the SubModule")],
    name_router: Annotated[str, typer.Argument(help="Name of the router")], 
):
    config = load_config()
    submodule: SubModule = config.get_submodule_by_name(name_submodule)

    if not submodule.get_router_by_name(name_router):
        console.print(f"💥 [red] {name_router} router not exist ! [/]")
        raise typer.Exit(code=1)

    router: Router = submodule.get_router_by_name(name_router)

    if not router:
        console.print(f"💥 [red] {name_router} router not exist ! [/]")
        raise typer.Exit(code=1)

    delete_router_content(router, submodule, config)
    submodule.routers.remove(router)
    save_config(config)
