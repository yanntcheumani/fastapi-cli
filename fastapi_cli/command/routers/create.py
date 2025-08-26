import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path

from fastapi_cli.utils.config.config import load_config, Schema
from typing import List

app = typer.Typer()
console = Console()


@app.command()
def create():
    """
    Create router
    """
    config = load_config()
    
