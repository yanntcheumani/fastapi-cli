from pathlib import Path

from fastapi_cli.utils.config.config import load_config, Module, save_config, Config, SubModule, Schema


def _get_response_model(name_schema: str) -> str:

    if name_schema == "None":
        return ""
    
    return "response_model=" + name_schema + ","

def _get_name_url(name_url: str) -> str:
    if name_url == "":
        return ""
    if len(name_url) == 1 and name_url == "/":
        return ""
    
    if len(name_url) >= 1:
        return f"{name_url[0:] if name_url[0] == "/" else name_url}"
    return name_url


def _check_import(submodule_path: Path) -> None:
    """
    Check if 'List' from typing is imported in the file, if not, add it.
    """

    file_content = submodule_path.read_text().splitlines()

    found_typing_import = False
    list_already_imported = False

    for i, line in enumerate(file_content):
        if line.startswith("from typing import"):
            found_typing_import = True
            if "List" in line:
                list_already_imported = True
                break

            file_content[i] = line.rstrip() + ", List"
            list_already_imported = True
            break

    if not list_already_imported:
        if found_typing_import:
            pass
        else:
            file_content.insert(0, "from typing import List")

    submodule_path.write_text("\n".join(file_content))

def _import_schema(name_schema: str, submodule_path: Path):
    if "None" in name_schema:
        return
 
    with open(submodule_path, "r+", encoding="utf-8") as f:
        content = f.read()
        import_line = f"from schemas.{name_schema.replace("Out", "")} import {name_schema}"
        if import_line not in content:
            lines = content.splitlines()
            insert_index = 0

            for i, line in enumerate(lines):
                if line.startswith("from") or line.startswith("import"):
                    insert_index = i + 1

            lines.insert(insert_index, import_line)
            content = "\n".join(lines)

            f.seek(0)
            f.write(content)
            f.truncate()

def create_router_content(
    config: Config,
    name_method: str,
    name_router: str,
    name_url: str,
    name_schema: str,
    submodule: SubModule
):
    url = _get_name_url(name_url)
    file_content = f"""\n
@router.{name_method}(
    "/{url}",
    status_code=status.HTTP_200_OK,
    {_get_response_model(name_schema)} 
    tags=["{submodule.name_module}:{submodule.name}"]
)
async def {name_router}():
    return """ + "{}"

    submodule_path = Path(submodule.path)

    if "List" in name_schema:
        _check_import(name_schema, submodule_path)
    
    if submodule_path.exists():
        with open(submodule_path, "a", encoding="utf-8") as f:
            f.write(file_content)
    else:
        with open(submodule_path, "w", encoding="utf-8") as f:
            f.write("from fastapi import APIRouter, status\n\n")
            f.write("router = APIRouter()\n")
            f.write(file_content)
    
    _import_schema(name_schema, submodule_path)
