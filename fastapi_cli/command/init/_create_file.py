from pathlib import Path
from rich.console import Console


console = Console()


def create_file(base, directory_path = Path("fastapi_cli/default_archi")):
    for file in directory_path.iterdir():
        new_file = base / file.name

        if file.is_file():
            new_file.write_text(file.read_text())
            console.print(f"📝 Created file: [cyan]{new_file}[/cyan]")

        if file.is_dir():
            create_file(new_file, file)
