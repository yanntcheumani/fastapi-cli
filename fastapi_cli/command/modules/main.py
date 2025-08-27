import typer
from rich.console import Console

from fastapi_cli.command.modules import create, list
from fastapi_cli.command.modules.submodules.main import app as submodule_app


app = typer.Typer()
app.add_typer(create.app, short_help="Command to create Routers")
app.add_typer(list.app, short_help="Command to List all modules")
app.add_typer(submodule_app, name="submodules", short_help="Command to Manage submodule")

console = Console()

