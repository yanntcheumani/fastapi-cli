import typer
from fastapi_cli.command.init import main as init
from fastapi_cli.command.run import main as run
from fastapi_cli.command.schemas import main as schemas

app = typer.Typer()

app.add_typer(init.app)
app.add_typer(run.app, name="run", short_help="Command to run the application")
app.add_typer(schemas.app, name="schemas", short_help="Command to manage Schemas")


def main():
    app()
