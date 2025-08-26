import typer
from fastapi_cli.command.init import main as init
from fastapi_cli.command.run import main as run
from fastapi_cli.command.schemas import main as schemas
from fastapi_cli.command.routers import main as routers
from fastapi_cli.command.modules import main as modules

app = typer.Typer()

app.add_typer(init.app)
app.add_typer(run.app, name="run", short_help="Command to run the application")
app.add_typer(schemas.app, name="schemas", short_help="Command to manage Schemas")
app.add_typer(modules.app, name="modules", short_help="Command to manage module")
app.add_typer(routers.app, name="routers", short_help="Command to manage router")

def main():
    app()
