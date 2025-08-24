import shutil
from pathlib import Path
import pytest
from typer.testing import CliRunner

from fastapi_cli.cli import app
from fastapi_cli.utils.config.config import load_config, save_config, Config, Schema, Module, NAME_CONFIG_FILE
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


def test_create_schema_file():
    """Test création d'un schema avec la commande create"""
    project_name = init_project()

    result = runner.invoke(app, ["schemas", "create", "User"])
    assert result.exit_code == 0

    schema_file = Path(f"{project_name}/schemas/User.py")
    assert schema_file.exists()
    content = schema_file.read_text()
    assert "class UserBase(BaseModel)" in content

    config = load_config()
    assert any(s.name == "User" for s in config.schemas)


def test_create_schema_already_exists():
    """Test si la commande échoue si un schema existe déjà"""
    project_name = init_project()
    Path(f"{project_name}/schemas/User.py").write_text("# dummy")

    result = runner.invoke(app, ["schemas", "create", "User"])

    assert result.exit_code != 0
    assert "file not created" in result.stdout


