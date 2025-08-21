from rich.console import Console
from pathlib import Path

console = Console()

def create_directory(base, directory_path = Path("fastapi_cli/default_archi")) -> None:
    for directory in directory_path.iterdir():
        if directory.is_dir():
            path = base / directory.name
            path.mkdir(parents=True, exist_ok=True)
            console.print(f"📂 Created directory: [blue]{path}[/blue]")
            create_directory(path, directory)
