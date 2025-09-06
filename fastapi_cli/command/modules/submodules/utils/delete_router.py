from pathlib import Path
import re
from pathlib import Path
from rich.console import Console

from fastapi_cli.utils.config.config import Router, load_config, Module, save_config, Config, SubModule, Schema

console = Console()

def delete_router_content(
        router: Router,
        submodule: SubModule,
        config: Config,
):
    file_content = f"""\n
@router.{router.method}(
    "/{router.url_name}",
    status_code=status.HTTP_200_OK,
)"""

    submodule_path = Path(submodule.path)

    if not submodule_path.exists():
        raise FileNotFoundError(f"Router file not found: {submodule_path}")

    with open(submodule_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        rf"@router\.{router.method}\(\s*['\"]/{router.url_name}['\"].*?\)\s*async def .*?:.*?(?=\n@router|\Z)",
        re.DOTALL
    )

    new_content, n = pattern.subn("", content)

    if n == 0:
        console.print(f"[red]❌ Aucun endpoint trouvé pour [bold]{router.method.upper()} /{router.url_name}[/bold] dans [cyan]{submodule.name}[/cyan][/red]")
        return

    with open(submodule_path, "w", encoding="utf-8") as f:
        f.write(new_content.strip() + "\n")

    console.print(f"[green]🗑️ Endpoint [bold]{router.method.upper()} /{router.url_name}[/bold] supprimé avec succès de [cyan]{submodule.name}[/cyan][/green]")

