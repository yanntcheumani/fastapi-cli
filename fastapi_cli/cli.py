import typer
from fastapi_cli import init

app = typer.Typer()
app.add_typer(init.init_app)


def main():
    app()
