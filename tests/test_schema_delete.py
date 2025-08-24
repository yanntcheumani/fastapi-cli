import pytest
from pathlib import Path
from unittest.mock import MagicMock
from typer.testing import CliRunner
import shutil

from fastapi_cli.cli import app
from fastapi_cli.command.schemas.update import _update_files 
from fastapi_cli.utils.config.config import Schema, load_config, NAME_CONFIG_FILE, save_config
from tests import CommandCli

runner = CliRunner()

def init_project(name="backend"):
    """Helper: initialise un projet avant les tests"""
    result = runner.invoke(app, [CommandCli.init.value, "--project-name", name])
    assert result.exit_code == 0
    return name

@pytest.fixture(autouse=True)
def cleanup():
    """Nettoyage automatique après chaque test"""
    yield
    for d in ["backend"]:
        if Path(d).exists():
            shutil.rmtree(d)
    if Path(NAME_CONFIG_FILE).exists():
        Path(NAME_CONFIG_FILE).unlink()



def test_delete_schema_success(monkeypatch):
    """Test si la suppression d'un fichier fonctionne"""
    init_project()

    res = runner.invoke(app, ["schemas", "create", "User"])
    assert res.exit_code == 0

    user_path_file = Path("backend/schemas/User.py")
    assert user_path_file.exists()  
    monkeypatch.setattr(
        "fastapi_cli.utils.config.config.Config.get_name_of_schemas",
        lambda self: ["User"],
    )

    monkeypatch.setattr(
        "fastapi_cli.utils.config.config.Config.get_schema",
        lambda self, name: Schema(name="User", path=str(user_path_file)),
    )

    class FakeSelect:
        def execute(self):
            return "User"

    monkeypatch.setattr(
        "InquirerPy.inquirer.select",
        lambda **kwargs: FakeSelect(),
    )

    monkeypatch.setattr("typer.confirm", lambda *args, **kwargs: True)

    result = runner.invoke(app, ["schemas", "delete"])

    assert result.exit_code == 0
    assert not user_path_file.exists()

def test_delete_schema_abort(monkeypatch):
    init_project()
    runner.invoke(app, ["schemas", "create", "User"])

    monkeypatch.setattr(
        "fastapi_cli.utils.config.config.Config.get_name_of_schemas",
        lambda self: ["User"],
    )
    monkeypatch.setattr(
        "fastapi_cli.utils.config.config.Config.get_schema",
        lambda self, name: Schema(name="User", path="backend/schemas/User.py"),
    )

    class FakeSelect:
        def execute(self): return "User"
    monkeypatch.setattr("InquirerPy.inquirer.select", lambda **kwargs: FakeSelect())
    monkeypatch.setattr("typer.confirm", lambda *a, **k: False)

    res = runner.invoke(app, ["schemas", "delete"])
    assert res.exit_code == 0  # tu raises Exit(0) sur abort

def test_delete_no_schemas(monkeypatch):
    init_project()
    # Force la liste vide
    monkeypatch.setattr(
        "fastapi_cli.utils.config.config.Config.get_name_of_schemas",
        lambda self: [],
    )
    res = runner.invoke(app, ["schemas", "delete"])
    assert res.exit_code == 1
    assert "No schemas found" in res.stdout


# def test_delete_no_schema(monkeypatch):
#     """Test quand aucun schéma n’existe"""

#     class EmptyConfig:
#         def get_name_of_schemas(self): return []
#         def get_schema(self, name): return None

#     monkeypatch.setattr("fastapi_cli.commands.delete.config", EmptyConfig())

#     result = runner.invoke(delete.app, ["delete"])

#     assert result.exit_code == 1
#     assert "no schemas found" in result.stdout.lower()
