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


def test_update_files_changes_content():
    init_project()

    result = runner.invoke(app, ["schemas", "create", "User"])
    assert result.exit_code == 0

    config = load_config()
    schema = config.get_schema("User")
    new_name: str = "AccountSchema"
    new_path = Path("backend/" + "schemas/" + new_name + ".py")

    _update_files(new_name, schema)

    assert "AccountSchema" in new_path.read_text()
    assert new_path.exists()
    assert schema.path == str(new_path)

