import logging
import os
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from pytest import LogCaptureFixture

from app.main import app, download_file
from app.model import DownloadRequest
from app.utils import render_template

CUR_DIR = os.path.dirname(os.path.realpath(__file__))


def test_uvicorn_error_logger_warning_when_convert_raises_value_err(
    caplog: LogCaptureFixture,
):
    # Positive case
    client = TestClient(app)
    payload = {"filename": ["test"], "content": [['{"diagram": "ClassDiagram"}']]}

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
    payload = {"filename": ["test"], "content": [[content]]}

    with caplog.at_level(logging.WARNING, "uvicorn.error"):
        client.post("/convert", json=payload)
        assert len(caplog.records) == 0


def test_uvicorn_error_logger_no_warning_convert_unexpected_error(
    caplog: LogCaptureFixture,
):
    # Edge case
    client = TestClient(app)
    payload = {"filename": ["test"], "content": [['{"diagram": "ClassDiagram"}']]}

    with caplog.at_level(logging.WARNING, "uvicorn.error"):
        with patch("app.main.ModelsElements") as mock_models:
            mock_instance_models = mock_models.return_value
            mock_instance_models.parse.side_effect = Mock(
                side_effect=NotImplementedError("some unexpected error")
            )
            with pytest.raises(NotImplementedError) as exc_info:
                client.post("/convert", json=payload)

        assert len(caplog.records) == 0
        assert str(exc_info.value) == "some unexpected error"


@pytest.mark.asyncio
async def test_uvicorn_error_logger_warning_when_download_file_bad_filename(
    caplog: LogCaptureFixture,
):
    # Positive case
    req = DownloadRequest(filename="/etc/passwd", content="abcd", type="abcd")
    with caplog.at_level(logging.WARNING, "uvicorn.error"):
        try:
            await download_file(req)
        except HTTPException:
            # already tested in test_main.py
            pass

        assert len(caplog.records) == 1
        assert (
            "uvicorn.error",
            logging.WARNING,
            "Bad filename: /etc/passwd",
        ) in caplog.record_tuples


@pytest.mark.asyncio
async def test_uvicorn_error_logger_warning_when_download_file_file_exists(
    caplog: LogCaptureFixture,
):
    # Positive case
    req = DownloadRequest(filename="abcd", content="abcd", type="abcd")
    with caplog.at_level(logging.WARNING, "uvicorn.error"):
        try:
            with patch("app.main.os.path.exists") as mock_exists:
                mock_exists.return_value = True
                await download_file(req)
        except HTTPException:
            # already tested in test_main.py
            pass

        assert len(caplog.records) == 1
        assert (
            "uvicorn.error",
            logging.WARNING,
            "File already exists: abcdabcd.py",
        ) in caplog.record_tuples


@pytest.mark.asyncio
async def test_uvicorn_error_logger_info_when_download_file_success(
    caplog: LogCaptureFixture,
):
    # Positive case
    req = DownloadRequest(filename="abcd", content="abcd", type="abcd")
    with caplog.at_level(logging.INFO, "uvicorn.error"):
        with patch("app.main.anyio.open_file") as mock_anyio:
            mock_anyio.return_value = AsyncMock()
            await download_file(req)

        assert len(caplog.records) == 1
        assert (
            "uvicorn.error",
            logging.INFO,
            "Finished writing: abcdabcd.py",
        ) in caplog.record_tuples


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
