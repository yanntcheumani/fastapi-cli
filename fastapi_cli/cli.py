import typer
from fastapi_cli.command.init import main as init
from fastapi_cli.command.run import main as run

app = typer.Typer()

app.add_typer(init.app)
app.add_typer(run.app, name="run", short_help="Command to run the application")


def main():
    app()
