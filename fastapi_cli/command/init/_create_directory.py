from rich.console import Console
from pathlib import Path
import importlib.resources as resources

console = Console()

def create_directory(base: Path, directory_path = None) -> None:

    if directory_path is None:
        with resources.path("fastapi_cli", "default_archi") as p:
            directory_path = p

    for directory in directory_path.iterdir():
        if directory.is_dir() and directory.name != "v1":
            path = base / directory.name
            path.mkdir(parents=True, exist_ok=True)
            console.print(f"📂 Created directory: [blue]{path}[/blue]")
            create_directory(path, directory)
