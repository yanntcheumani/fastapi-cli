import pytest
from typer.testing import CliRunner
from fastapi_cli.cli import app
import shutil
from pathlib import Path
from tests import CommandCli

runner = CliRunner()


@pytest.fixture(autouse=True)
def cleanup():
    """Nettoyage automatique des dossiers créés pendant les tests"""
    yield
    if Path("myproject").exists():
        shutil.rmtree("myproject")
    if Path("testproject").exists():
        shutil.rmtree("testproject")
    if Path("backend").exists():
        shutil.rmtree("backend")


def test_init_with_name():
    """Test création projet avec un nom passé en argument"""
    result = runner.invoke(app, [CommandCli.init.value, "--project-name", "myproject"])

    assert result.exit_code == 0
    assert Path("myproject").exists()
    assert Path("myproject/main.py").exists()
    assert Path("myproject/schemas").exists()


def test_init_prompt(monkeypatch):
    """Test création projet avec input utilisateur"""

    monkeypatch.setattr("typer.prompt", lambda text: "backend")
    result = runner.invoke(app, [CommandCli.init.value])
    
    assert result.exit_code == 0
    assert Path("backend/schemas").exists()
    assert Path("backend/api").exists()
    assert Path("backend/db").exists()

def test_init_existing_directory():
    """Test si le projet existe déjà"""
    Path("myproject").mkdir()
    result = runner.invoke(app, [CommandCli.init.value, "--project_name", "myproject"])

    assert result.exit_code != 0

