import typer
from rich.console import Console
import uvicorn
from pathlib import Path

from fastapi_cli.utils.config.config import Config, load_config
from fastapi_cli.command.schemas import create
from fastapi_cli.command.schemas import list

app = typer.Typer()
app.add_typer(create.app, short_help="Command to create Schema")
app.add_typer(list.app, short_help="List all Schemas")


console = Console()
config = load_config()

