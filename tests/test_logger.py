import json
import logging
import logging.config
import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient
from pytest import LogCaptureFixture

from app.main import app
from app.utils import render_template

CUR_DIR = os.path.dirname(os.path.realpath(__file__))


def test_uvicorn_error_logger_warning_when_convert_raises_value_err(
    caplog: LogCaptureFixture,
):
    # Positive case
    client = TestClient(app)
    payload = {
        "filename": ["test"],
        "content": [['{"diagram": "ClassDiagram"}']],
        "project_name": "test",
    }

    with caplog.at_level(logging.WARNING, "uvicorn.error"):
        with patch("app.main.ModelsElements") as mock_models:
            mock_instance_models = mock_models.return_value
            mock_instance_models.parse.side_effect = Mock(
                side_effect=ValueError("some error")
            )
            client.post("/convert", json=payload)

        assert len(caplog.records) == 1
        assert (
            "uvicorn.error",
            logging.WARNING,
            "Error occurred at parsing: some error",
        ) in caplog.record_tuples


def test_uvicorn_error_logger_no_warning_when_convert_success(
    caplog: LogCaptureFixture,
):
    # Negative case
    client = TestClient(app)
    with open(os.path.join(CUR_DIR, "test_input.txt")) as f:
        content = f.read().strip()
    payload = {"filename": ["test"], "content": [[content]], "project_name": "test"}

    with caplog.at_level(logging.WARNING, "uvicorn.error"):
        client.post("/convert", json=payload)
        assert len(caplog.records) == 0


def test_uvicorn_error_logger_no_warning_convert_unexpected_error(
    caplog: LogCaptureFixture,
):
    # Edge case
    client = TestClient(app)
    payload = {
        "filename": ["test"],
        "content": [['{"diagram": "ClassDiagram"}']],
        "project_name": "test",
    }

    with caplog.at_level(logging.WARNING, "uvicorn.error"):
        with patch("app.main.ModelsElements") as mock_models:
            mock_instance_models = mock_models.return_value
            mock_instance_models.parse.side_effect = Mock(
                side_effect=NotImplementedError("some unexpected error")
            )
            resp = client.post("/convert", json=payload)

        assert len(caplog.records) == 1
        assert (
            "uvicorn.error",
            logging.WARNING,
            "Unknown error occured: some unexpected error",
        ) in caplog.record_tuples
        assert (
            resp.json()["detail"]
            == "Unknown error occured: some unexpected error\nPlease try again later"
        )
        assert resp.status_code == 500


def test_uvicorn_error_logger_error_when_template_not_found(
    caplog: LogCaptureFixture,
):
    # Positive case
    with caplog.at_level(logging.ERROR, "uvicorn.error"):
        render_template("a", {})

        assert len(caplog.records) == 1
        assert (
            "uvicorn.error",
            logging.ERROR,
            "Template not found: a",
        ) in caplog.record_tuples


def test_uvicorn_error_logger_warning_when_unexpected_exception(
    caplog: LogCaptureFixture,
):
    # Positive case
    with patch("app.utils.env.get_template") as mock_template:
        mock_template.return_value = Mock()
        mock_template.return_value.render.side_effect = Mock(
            side_effect=KeyError("somehow key error occured")
        )
        with caplog.at_level(logging.WARNING, "uvicorn.error"):
            render_template("models.py.j2", {})

            assert len(caplog.records) == 1
            assert (
                "uvicorn.error",
                logging.WARNING,
                "An error occured: 'somehow key error occured'",
            ) in caplog.record_tuples


def test_uvicorn_error_logger_warning_when_invalid_group_id(caplog: LogCaptureFixture):
    client = TestClient(app)
    payload = {
        "filename": ["test"],
        "content": [['{"diagram": "ClassDiagram"}']],
        "project_name": "test",
        "project_type": "spring",
        "group_id": ".abcd",
    }
    with caplog.at_level(logging.WARNING, "uvicorn.error"):
        client.post("/convert", json=payload)

        assert len(caplog.records) == 1
        assert (
            "uvicorn.error",
            logging.WARNING,
            "Invalid Java package name: test..abcd",
        ) in caplog.record_tuples


@pytest.fixture
def uvicorn_log_config(tmp_path: Path) -> tuple[dict, Path]:
    """Load the uvicorn logging config with temp directories"""
    config_path = "logger_conf.json"
    with open(config_path) as f:
        config = json.load(f)

    # Update paths to use temp directory
    log_dir = tmp_path / "logs"
    log_dir.mkdir()

    config["handlers"]["default"]["filename"] = str(log_dir / "convert.log")
    config["handlers"]["access"]["filename"] = str(log_dir / "convert_access.log")

    return config, log_dir


def test_uvicorn_error_access_log_config_creates_file(
    uvicorn_log_config: tuple[dict, Path],
):
    config, log_dir = uvicorn_log_config
    logging.config.dictConfig(config)
    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_access = logging.getLogger("uvicorn.access")

    uvicorn_error.error("Some error occured!")
    uvicorn_access.info("%s%s%s%s%s", "127.0.0.1", "GET", "/", "1.1", "200")

    assert (log_dir / "convert.log").exists()
    assert (log_dir / "convert_access.log").exists()

    with open(log_dir / "convert.log") as f:
        content = f.read()
        assert "Some error occured!" in content

    with open(log_dir / "convert_access.log") as f:
        content = f.read()
        assert "GET /" in content
        assert "200" in content
        assert "127.0.0.1" in content


def test_uvicorn_error_access_rotate_when_near_capacity(
    uvicorn_log_config: tuple[dict, Path],
):
    config, log_dir = uvicorn_log_config
    config["handlers"]["default"]["maxBytes"] = 1024
    config["handlers"]["access"]["maxBytes"] = 1024

    logging.config.dictConfig(config)
    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_access = logging.getLogger("uvicorn.access")

    uvicorn_error.error("A" * 512)
    uvicorn_error.error("A" * 600)
    uvicorn_access.info(
        "%s%s%s%s%s", "127.0.0.1", "GET", "/" + ("A" * 512), "1.1", "200"
    )
    uvicorn_access.info(
        "%s%s%s%s%s", "127.0.0.1", "GET", "/" + ("A" * 600), "1.1", "200"
    )

    assert len(list(log_dir.glob("convert.log.*"))) > 0
    assert len(list(log_dir.glob("convert_access.log.*"))) > 0


def test_uvicorn_error_access_max_backup_five(uvicorn_log_config: tuple[dict, Path]):
    config, log_dir = uvicorn_log_config
    config["handlers"]["default"]["maxBytes"] = 1024
    config["handlers"]["access"]["maxBytes"] = 1024

    logging.config.dictConfig(config)
    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_access = logging.getLogger("uvicorn.access")

    for _ in range(10):
        uvicorn_error.error("A" * 512)
        uvicorn_access.info(
            "%s%s%s%s%s", "127.0.0.1", "GET", "/" + ("A" * 512), "1.1", "200"
        )

    assert len(list(log_dir.glob("convert.log.*"))) == 5
    assert len(list(log_dir.glob("convert_access.log.*"))) == 5
