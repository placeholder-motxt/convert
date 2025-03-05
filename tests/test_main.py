import os
from unittest.mock import AsyncMock, MagicMock, patch

import anyio
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI World!"}


@pytest.fixture
def test_file() -> dict:
    """Provides a test file name and content"""
    return {"filename": "testfile", "content": "print('Hello, world!')"}


def test_download_file(test_file: dict):
    """Test the /download/ endpoint"""

    response = client.post("/download/", json=test_file)

    assert response.status_code == 200

    downloaded_content = response.content.decode("utf-8")
    assert downloaded_content == test_file["content"]

    file_path = test_file["filename"] + ".py"
    assert not os.path.exists(file_path)


def test_file_already_exists():
    with open("a.py", "w") as f:
        f.write("Some initial content")

    try:
        # Try to upload a file
        response = client.post(
            "/download/", json={"filename": "a", "content": "Some content"}
        )
        assert response.status_code, 400
        assert response.json()["detail"], "The file already exists."
    finally:
        # Clean up: remove the file created for the test
        if os.path.exists("a.py"):
            os.remove("a.py")


def test_slash_on_filename():
    # Try to upload a file
    response = client.post(
        "/download/", json={"filename": "app/main2", "content": "Some content"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "/ not allowed"


@pytest.mark.asyncio
async def test_convert_endpoint_empty_content():
    # Mock ParseJsonToObjectClass to avoid executing its real implementation
    with patch("app.parse_json_to_object_class.ParseJsonToObjectClass") as MockParser:
        mock_instance = MockParser.return_value
        mock_instance.parse_classes.return_value = [
            MagicMock(to_models_code=MagicMock(return_value="class Test {}"))
        ]
        mock_instance.parse_relationships.return_value = None

        # Mock httpx.AsyncClient to prevent real HTTP requests
        with patch("httpx.AsyncClient") as MockClient:
            mock_client_instance = MockClient.return_value
            mock_post = AsyncMock()
            mock_post.return_value.content = b"mocked response"
            mock_post.return_value.headers = {"content-type": "text/plain"}
            mock_client_instance.__aenter__.return_value.post = mock_post

            # Prepare the request payload with the necessary 'nodes' key
            payload = {
                "filename": "test.txt",
                "content": '{"nodes": [],"edges":[]}',  # Ensure 'nodes' key is present
            }

            # Send the request to the endpoint
            response = client.post("/convert", json=payload)

            # Validate the response
            assert response.status_code == 200
            assert response.content == b"mocked response"
            assert response.headers["content-type"] == "text/plain; charset=utf-8"

            # Ensure the mocked post request was called with expected parameters
            mock_post.assert_called_once_with(
                "/download/", json={"filename": "test.txt", "content": ""}
            )


@pytest.mark.asyncio
async def test_convert_endpoint_valid_content():
    # Mock ParseJsonToObjectClass to avoid executing its real implementation
    with patch("app.parse_json_to_object_class.ParseJsonToObjectClass") as MockParser:
        mock_instance = MockParser.return_value
        mock_instance.parse_classes.return_value = [
            MagicMock(to_models_code=MagicMock(return_value="class Test {}"))
        ]
        mock_instance.parse_relationships.return_value = None

        # Mock httpx.AsyncClient to prevent real HTTP requests
        with patch("httpx.AsyncClient") as MockClient:
            mock_client_instance = MockClient.return_value
            mock_post = AsyncMock()
            mock_post.return_value.content = b"mocked response"
            mock_post.return_value.headers = {"content-type": "text/plain"}
            mock_client_instance.__aenter__.return_value.post = mock_post

            async with await anyio.open_file("tests/test_input.txt") as f:
                async with await anyio.open_file("tests/test_result.txt") as f2:
                    test_case = await f.read()
                    test_case_result = await f2.read()
                    # Prepare the request payload with the necessary 'nodes' key
                    payload = {"filename": "file1", "content": test_case}

                    # Send the request to the endpoint
                    response = client.post("/convert", json=payload)

                    # Validate the response
                    assert response.status_code == 200
                    assert response.content == b"mocked response"
                    assert (
                        response.headers["content-type"] == "text/plain; charset=utf-8"
                    )

                    # Ensure the mocked post request was called with expected parameters
                    mock_post.assert_called_once_with(
                        "/download/",
                        json={"filename": "file1", "content": test_case_result},
                    )
