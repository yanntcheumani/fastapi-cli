import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
from typing_extensions import Annotated

from fastapi_cli.utils.config.config import load_config, Module, Config, SubModule, Router

app = typer.Typer()
console = Console()

@app.command()
def list(name: Annotated[str, typer.Argument(help="Module name (optional). If empty, shows all modules.")] = ""):
    """
    List all modules and their contents (submodules, schemas, services, routers).
    """
    config: Config = load_config()
    modules = config.modules

    if not modules:
        console.print("[bold red]No modules found in the configuration[/bold red]")
        raise typer.Exit(code=1)

    for module in modules:
        if name and module.name != name:
            continue

        table = Table(title=f"📦 Module [bold cyan]{module.name}[/bold cyan] (v{module.version})", show_lines=True)
        table.add_column("Type", style="bold yellow")
        table.add_column("Name", style="bold green")
        table.add_column("Details", style="white")

        # Submodules
        if module.submodules:
            for sub in module.submodules:
                table.add_row("SubModule", sub.name or "-", "-")
                # Schemas
                if sub.schemas:
                    for schema in sub.schemas:
                        table.add_row(" └─ Schema", schema.name, schema.path)
                # Services
                if sub.services:
                    for service in sub.services:
                        table.add_row(" └─ Service", service.name, service.path)
                # Routers
                if sub.routers:
                    for router in sub.routers:
                        table.add_row(" └─ Router", router.router_name, f"{router.method.upper()} {router.path} {router.url_name} (schema={router.schema})")

        console.print(table)

@app.command()
def details(module_name: Annotated[str, typer.Argument(help="Name of the module to inspect")]):
    """
    Show details of a specific module: submodules, schemas, services, routes.
    """
    config: Config = load_config()
    module = next((m for m in config.modules if m.name == module_name), None)

    if not module:
        console.print(f"[bold red]❌ Module '{module_name}' not found[/bold red]")
        raise typer.Exit(code=1)

    table = Table(title=f"🔎 Module details [bold cyan]{module.name}[/bold cyan]", show_lines=True)
    table.add_column("SubModule", style="bold yellow")
    table.add_column("Schemas", style="green")
    table.add_column("Services", style="blue")
    table.add_column("Routers", style="magenta")

    if module.submodules:
        for sub in module.submodules:
            schemas = "\n".join([s.name for s in sub.schemas]) if sub.schemas else "-"
            services = "\n".join([s.name for s in sub.services]) if sub.services else "-"
            routers = "\n".join([f"{r.method.upper()} {r.path}" for r in sub.routers]) if sub.routers else "-"
            table.add_row(sub.name or "-", schemas, services, routers)

    console.print(table)