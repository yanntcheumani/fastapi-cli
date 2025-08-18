import typer

app = typer.Typer()


@app.command()
def init(project_name: str = "backend"):
    typer.echo(f"initialation du project avec comme nom {project_name}")



def main():
    app()
