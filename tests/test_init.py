import pytest
from typer.testing import CliRunner
from fastapi_cli.cli import app
import shutil
from pathlib import Path
from tests import CommandCli

runner = CliRunner()


import shutil
from pathlib import Path
import pytest
from typer.testing import CliRunner

from fastapi_cli.utils.config.config import load_config, NAME_CONFIG_FILE

runner = CliRunner()


@pytest.fixture(autouse=True)
def cleanup():
    """Nettoyage automatique des dossiers créés pendant les tests"""
    yield
    for d in ["myproject", "testproject", "backend"]:
        if Path(d).exists():
            shutil.rmtree(d)
    if Path(NAME_CONFIG_FILE).exists():
        Path(NAME_CONFIG_FILE).unlink()


def test_init_with_name():
    """Test création projet avec un nom passé en argument"""
    result = runner.invoke(app, [CommandCli.init.value, "--project-name", "myproject"])

    assert result.exit_code == 0
    assert Path("myproject").exists()
    assert Path("myproject/main.py").exists()
    assert Path("myproject/schemas").exists()

    config_path = Path(NAME_CONFIG_FILE)
    assert config_path.exists()
    config = load_config(config_path)
    assert config.ProjectName == "myproject"
    assert config.schemas == []
    assert config.modules == []


def test_init_prompt(monkeypatch):
    """Test création projet avec input utilisateur"""
    monkeypatch.setattr("typer.prompt", lambda text: "backend")
    result = runner.invoke(app, [CommandCli.init.value])

    assert result.exit_code == 0
    assert Path("backend/schemas").exists()
    assert Path("backend/api").exists()
    assert Path("backend/db").exists()

    config = load_config()
    assert config.ProjectName == "backend"
    assert config.schemas == []
    assert config.services == []


def test_init_existing_directory():
    """Test si le projet existe déjà"""

    Path("myproject").mkdir()
    result = runner.invoke(app, [CommandCli.init.value, "--project-name", "myproject"])

    assert result.exit_code != 0

    assert not Path(NAME_CONFIG_FILE).exists()
