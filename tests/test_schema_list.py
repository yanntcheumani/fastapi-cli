import shutil
from pathlib import Path
import pytest
from typer.testing import CliRunner

from fastapi_cli.cli import app
from fastapi_cli.utils.config.config import load_config, save_config, Config, Schema, Module, NAME_CONFIG_FILE, SubModule
from tests import CommandCli

runner = CliRunner()


@pytest.fixture(autouse=True)
def cleanup():
    """Nettoyage automatique après chaque test"""
    yield
    for d in ["backend"]:
        if Path(d).exists():
            shutil.rmtree(d)
    if Path(NAME_CONFIG_FILE).exists():
        Path(NAME_CONFIG_FILE).unlink()


def init_project(name="backend"):
    """Helper: initialise un projet avant les tests"""
    result = runner.invoke(app, [CommandCli.init.value, "--project-name", name])
    assert result.exit_code == 0
    return name


def test_list_no_schemas(monkeypatch):
    """Test list quand aucun schema n'existe"""
    init_project()

    result = runner.invoke(app, ["schemas", "list"])

    assert result.exit_code == 0
    assert "No schemas found" in result.stdout


def test_list_with_schemas():
    """Test list avec schemas dans config"""
    project_name = init_project()

    schema = Schema(name="Product", path=f"{project_name}/schemas/Product.py")
    config = load_config()
    config.schemas.append(schema)
    save_config(config)

    result = runner.invoke(app, ["schemas", "list"])

    assert result.exit_code == 0
    assert "Product" in result.stdout
    assert "Config" in result.stdout


def test_list_with_module_schemas():
    """Test list avec schemas dans un module"""
    project_name = init_project()

    schema = {"name": "Order", "path": f"{project_name}/schemas/Order.py"}
    module = Module(submodules=[], name="sales")
    submodule = SubModule(schemas=[schema], routers=[], name="User", services=[], name_module=module.name, path="")
    module.submodules.append(submodule)
    config = load_config()
    config.modules.append(module)
    save_config(config)

    result = runner.invoke(app, ["schemas", "list"])

    assert result.exit_code == 0
    assert "Order" in result.stdout
    assert "Module: sales" in result.stdout
