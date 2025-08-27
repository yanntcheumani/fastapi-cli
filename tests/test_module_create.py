import pytest
from typer.testing import CliRunner
from pathlib import Path
import shutil

from fastapi_cli.cli import app as init_app
from fastapi_cli.command.modules.create import app, _add_module_in_routers, _create_module
from fastapi_cli.utils.config.config import Config, Module, save_config, NAME_CONFIG_FILE, load_config
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
    result = runner.invoke(init_app, [CommandCli.init.value, "--project-name", name])
    assert result.exit_code == 0
    return name

def test_add_module_in_routers_success():
    init_project()
    config = load_config()
    name_path = Path(config.ProjectName + "/api/v2")


    module = Module([], "v2", 1)
    name_path.mkdir()
    _create_module(config, name_path, module)
    ok = _add_module_in_routers(module, config)
    assert ok is True

    routers_content = Path(config.ProjectName + "/api/routers.py").read_text()
    assert "from api.v2.router import router_v2" in routers_content
    assert "routers.include_router(router_v2" in routers_content


def test_add_module_in_routers_fail():
    init_project()
    config = load_config()
    module = Module([], "bad", 2)

    Path(config.ProjectName + "/api/routers.py").unlink()
    ok = _add_module_in_routers(module, config)

    assert ok is False


def test_create_module_success():
    init_project()
    config = load_config()

    name_path = Path(config.ProjectName + "/api/user")
    name_path.mkdir()
    module = Module([], "user", 1)
    ok = _create_module(config, name_path, module)

    assert ok is True
    assert (name_path / "router.py").exists()
    assert (name_path / "endpoints").exists()


def test_create_module_fail_and_rollback():
    """
    Simule un échec en supprimant routers.py avant _create_module.
    """
    init_project()
    config = load_config()

    Path(config.ProjectName + "/api/routers.py").unlink()
    name_path = Path(config.ProjectName + "/api/v2")
    name_path.mkdir()
    module = Module([], "v2", 1)
    ok = _create_module(config, name_path, module)

    # doit retourner False et rollback
    assert ok is False
    assert not (name_path / "router.py").exists()
    assert not (name_path / "endpoints").exists()


def test_cli_create_module_with_name():
    init_project()
    config = load_config()

    result = runner.invoke(init_app, ["modules", "create", "user"], catch_exceptions=False)
    assert result.exit_code == 0
    assert "module created with success" in result.stdout

    created_router = Path(config.ProjectName + "/api/user/router.py")
    assert created_router.exists()


def test_cli_create_module_without_name():
    """
    Si aucun nom n'est donné, il doit prendre v + nombre de modules.
    """
    init_project()
    config = load_config()

    result = runner.invoke(init_app, ["modules", "create"], catch_exceptions=False)
    print("bonjour: ", result.output)

    assert result.exit_code == 0
    assert "module created with success" in result.stdout

    created_router = Path(config.ProjectName + "/api/v2/router.py")
    assert created_router.exists()


def test_cli_create_module_already_exist():
    init_project()
    config = load_config()

    runner.invoke(init_app, ["modules", "create", "user"])
    result = runner.invoke(init_app, ["modules", "create", "user"])
    assert result.exit_code == 1
    assert "module user already exist" in result.stdout
