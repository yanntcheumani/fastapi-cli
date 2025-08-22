import typer
from pathlib import Path
from rich.console import Console


from fastapi_cli.command.init._create_directory import create_directory
from fastapi_cli.command.init._create_file import create_file
from fastapi_cli.utils.config.config import Config, save_config

console = Console()
app = typer.Typer()


@app.command()
def init(project_name: str = typer.Option("", help="Nom du projet FastAPI")):
    """
    Initialise un nouveau projet FastAPI avec une structure par défaut.
    """
    console.print(":rocket: [bold green]Start of the initialization[/bold green]")

    if not project_name:
        project_name = typer.prompt(
            "What is the name of your API ?",
            #default="backend"
        )
    base = Path(project_name)

    if base.exists():
        console.print(f"❌ [red]Le dossier {project_name} existe déjà[/red]")
        raise typer.Exit(code=1)

    create_directory(base)
    create_file(base)
    
    config = Config(ProjectName=project_name, schemas=[], services=[], modules=[], isLoad=True)
    save_config(config)
    console.print(f"✅ [bold green]Project {project_name} created successfully![/bold green]")
    raise typer.Exit(code=0)