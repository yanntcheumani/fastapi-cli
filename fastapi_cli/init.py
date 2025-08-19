import typer
from pathlib import Path
from rich.console import Console

console = Console()
init_app = typer.Typer()

# Définition des dossiers et fichiers à créer
DIRECTORIES = [
    "api",
    "api/v1",
    "schemas",
    "crud",
    "services",
    "core",
    "db",
    "db/models"
]

FILES = {
    "db/session.py": "",
    "deps.py": "",
    "main.py": """from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
"""
}


@init_app.command()
def init(project_name: str = typer.Option("", help="Nom du projet FastAPI")):
    """
    Initialise un nouveau projet FastAPI avec une structure par défaut.
    """
    console.print(":rocket: [bold green]Start of the initialization[/bold green]")

    if not project_name:
        project_name = typer.prompt(
            "What is the name of your API ?",
            default="backend"
        )

    base = Path(project_name)

    if base.exists():
        console.print(f"❌ [red]Le dossier {project_name} existe déjà[/red]")
        raise typer.Exit(code=1)

    for directory in DIRECTORIES:
        path = base / directory
        path.mkdir(parents=True, exist_ok=True)
        console.print(f"📂 Created directory: [blue]{path}[/blue]")

    for filepath, content in FILES.items():
        file = base / filepath
        file.write_text(content)
        console.print(f"📝 Created file: [cyan]{file}[/cyan]")

    console.print(f"✅ [bold green]Project {project_name} created successfully![/bold green]")
    raise typer.Exit(code=0)