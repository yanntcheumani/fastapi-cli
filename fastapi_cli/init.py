import typer
from pathlib import Path

init_app = typer.Typer()


@init_app.command()
def init(project_name: str = "backend"):
    typer.echo(f"initialation du project avec comme nom {project_name}")

    base = Path(project_name)

    if base.exists():
        typer.echo(f"❌ Le dossier {project_name} existe déjà")
        raise typer.Exit(code=1)
    
    (base / "api").mkdir(parents=True, exist_ok=True)
    (base / "schemas").mkdir(parents=True, exist_ok=True)
    (base / "crud").mkdir(parents=True, exist_ok=True)
    (base / "services").mkdir(parents=True, exist_ok=True)
    (base / "models").mkdir(parents=True, exist_ok=True)
    (base / "models" / "__init__.py").write_text("")


    (base / "main.py").write_text(
        'from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get("/")\ndef read_root():\n    return {"Hello": "World"}\n'
    )
