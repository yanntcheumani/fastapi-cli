import typer
from rich.console import Console
from InquirerPy import inquirer
from typing import List
from rich.prompt import Prompt
from pathlib import Path
from typing import Union

from fastapi_cli.utils.config.config import load_config, Schema, save_config

app = typer.Typer()

console = Console()
config = load_config()

EXCLUDED_DIRS = {".git", "venv", "__pycache__", ".mypy_cache", ".idea", ".vscode"}

def _update_files(new_name: str, schema: Schema):
    root = Path(config.ProjectName)

    for path in root.rglob("*"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue

        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue

            if schema.name in text:
                new_text = text.replace(schema.name, new_name)
                path.write_text(new_text, encoding="utf-8")
                print(f"✅ file changed : {path}")

            if str(path).endswith(schema.path):
                new_path = path.with_name(new_name + path.suffix)
                path.rename(new_path)
                schema.path = str(new_path)
                print(f"📂 file rename : {path} → {new_path}")

@app.command()
def update():
    schemas: List[str] = config.get_name_of_schemas()

    if len(schemas) == 0:
        console.print("[yellow]No schemas found in config or modules.[/]")
        typer.Exit(code=1)

    name_schema: str = inquirer.select(
        message="Choose the Schema :",
        choices=schemas,
        default=schemas[0],
    ).execute()

    schema: Schema =  config.get_schema(name_schema)

    if not schema:
        console.print("[yellow]No schemas found in config or modules.[/]")
        typer.Exit(code=1)

    new_schema_name = Prompt.ask(f"What is the new name ? by default the wil be : ", default=name_schema)

    _update_files(new_schema_name, schema)
    schema.name = new_schema_name
    save_config(config)
