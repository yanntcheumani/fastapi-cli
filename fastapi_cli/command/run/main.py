import typer
from rich.console import Console
import uvicorn
from pathlib import Path

app = typer.Typer()
console = Console()

@app.command()
def dev(
    project_name: str = "backend",
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = True
):
    """
    Launches the FastAPI project in development mode with Uvicorn.
    """
    base = Path(project_name)
    main_file = base / "main.py"

    if not main_file.exists():
        console.print(f"❌ Unable to start the project: {main_file} not found")
        raise typer.Exit(code=1)

    console.print(f"🚀 Starting project {project_name} at http://{host}:{port} ...")

    uvicorn.run(
        f"main:app",
        host=host,
        port=port,
        reload=reload,
        app_dir=project_name
    )