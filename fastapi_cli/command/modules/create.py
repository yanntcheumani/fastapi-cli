import typer
from rich.console import Console
from pathlib import Path
from typing_extensions import Annotated

from fastapi_cli.utils.config.config import load_config, Module, save_config, Config

app = typer.Typer()
console = Console()

def _add_module_in_routers(module: Module, config: Config) -> bool:
    try:
        path_routers = Path(config.ProjectName + "/api/routers.py")
        routers_content = f"""
from api.{module.name}.router import router_{module.name}

routers.include_router(router_{module.name}, prefix="/{module.name}", tags=["{module.name}"])
"""
        if not path_routers.exists():
            console.print(f"💥 [red] erreur lors de l'ajout du module dans le routers [/]")
            return False
    
        with path_routers.open("a", encoding="utf-8") as f:
            f.write(routers_content)

        return True
    except:
        console.print(f"💥 [red] erreur lors de l'ajout du module dans le routers [/]")
        return False

def _create_module(config: Config, name_path: Path, module: Module) -> bool:
    name_path_endpoint = name_path / "endpoints"
    name_path_endpoint.mkdir()
    router_file_content = f"""
from fastapi import APIRouter

router_{module.name} = APIRouter()
"""

    name_path_router = name_path / "router.py"
    name_path_router.write_text(router_file_content)

    if not _add_module_in_routers(module, config):
        name_path_endpoint.rmdir()
        name_path_router.unlink()
        return False
    return True

@app.command()
def create(name: Annotated[str, typer.Argument(help="Name of the Module (by default it will be 'v' + number of module)")] = ""):
    """
    Create a new version of api
    """

    config = load_config()

    if name == "":
        name = "v" + str(len(config.modules) + 1)

    name_path = Path(config.ProjectName + "/api/" + name)
    
    if name_path.exists():
        console.print(f"💥 [red] module {name} already exist[/]")
        raise typer.Exit(code=1)

    name_path.mkdir()
    module = Module([], name, len(config.modules) + 1)
    if not _create_module(config, name_path, module):
        name_path.rmdir()
        raise typer.Exit(code=1)

    config.modules.append(module)
    save_config(config)
    console.print(f"💥 [green] module created with success ![/]")


    
    
