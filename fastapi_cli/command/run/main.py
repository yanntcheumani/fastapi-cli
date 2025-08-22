import typer
from rich.console import Console
import uvicorn
from pathlib import Path

from fastapi_cli.utils.config.config import Config, load_config

app = typer.Typer()
console = Console()
config = load_config()

@app.command()
def dev(
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = True
):
    """
    Launches the FastAPI project in development mode with Uvicorn.
    """

    main_file = Path(config.ProjectName) / "main.py"

    if not config.isLoad:
        console.print(f"unable to start the project because the config file is not set or it's corrupted")
        raise typer.Exit(code=1)

    if not main_file.exists():
        console.print(f"❌ Unable to start the project: {main_file} not found")
        raise typer.Exit(code=1)

    console.print(f"🚀 Starting project {config.ProjectName} at http://{host}:{port} ...")

    uvicorn.run(
        f"main:app",
        host=host,
        port=port,
        reload=reload,
        app_dir=config.ProjectName
    )