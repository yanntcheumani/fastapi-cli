import typer
from rich.console import Console
from pathlib import Path
from typing_extensions import Annotated

from fastapi_cli.utils.config.config import load_config, Schema, save_config

app = typer.Typer()


console = Console()
config = load_config()

@app.command()
def create(name: Annotated[str, typer.Argument(help="Name of the Schema", show_default=False)]):
    """
    Create a Schema file and structure with
    """
    

    schema = Schema(name=name)
    file = f"""
from pydantic import BaseModel

class {schema.name}Base(BaseModel):
    pass
    
class {schema.name}In({schema.name}Base):
    pass
class {schema.name}Out({schema.name}Base):
    pass
"""

    schema.path = config.ProjectName + "/" + schema.path + "/" + str(schema.name) + ".py"

    filepath = Path(schema.path)

    if filepath.exists():
        console.print(f"💥 file not created: [cyan]{schema.path}[/cyan]")
        raise typer.Exit(code=1)
    filepath.write_text(file)
    config.schemas.append(schema)
    save_config(config)

    console.print(f"📝 Created file: [cyan]{schema.path}[/cyan]")