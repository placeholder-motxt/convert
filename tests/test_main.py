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


def test_file_already_exists():
    with open("a.py", "w") as f:
        f.write("Some initial content")

    try:
        # Try to upload a file
        response = client.post(
            "/convert/", json={"filename": "a", "content": "Some content"}
        )
        assert response.status_code, 400
        assert response.json()["detail"], "The file already exists."
    finally:
        # Clean up: remove the file created for the test
        if os.path.exists("a.py"):
            os.remove("a.py")


def test_slash_on_filename():
    # Try to upload a file
    with patch("app.main.ModelsElements") as MockParser:
        with patch("app.main.ViewsElements") as MockParser2:
            mock_instance = MockParser.return_value
            mock_instance.parse.return_value = [
                MagicMock(to_models_code=MagicMock(return_value="class Test {}"))
            ]

            mock_instance.print_django_style.return_value = "ini class write"

            mock_instance = MockParser2.return_value
            mock_instance.add_class_method.return_value = [
                MagicMock(to_views_code=MagicMock(return_value="view Test {}"))
            ]

            mock_instance.print_django_style.return_value = "ini view write"

            response = client.post(
                "/convert/", json={"filename": "app/main2", "content": "Some content"}
            )
            assert response.status_code == 400
            assert response.json()["detail"] == "/ not allowed"


@pytest.mark.asyncio
async def test_convert_endpoint_valid_content():
    # Mock ParseJsonToObjectClass to avoid executing its real implementation
    with patch("app.main.ModelsElements") as MockParser:
        with patch("app.main.ViewsElements") as MockParser2:
            mock_instance = MockParser.return_value
            mock_instance.parse.return_value = [
                MagicMock(to_models_code=MagicMock(return_value="class Test {}"))
            ]

            mock_instance.print_django_style.return_value = "ini class write"

            mock_instance = MockParser2.return_value
            mock_instance.add_class_method.return_value = [
                MagicMock(to_views_code=MagicMock(return_value="view Test {}"))
            ]

            mock_instance.print_django_style.return_value = "ini view write"

            with patch("app.main.download_file") as MockClient:
                with patch("app.main.download_file") as MockClient2:
                    with (
                        patch("zipfile.ZipFile") as mock_zipfile,
                        patch("os.remove") as mock_remove,
                    ):
                        mock_zipf = (
                            mock_zipfile.return_value.__enter__.return_value
                        )  # Mock the context manager
                        mock_zipf.write = MagicMock()

                        mock_client_instance = MockClient.return_value
                        mock_post = AsyncMock()
                        mock_post.return_value.content = b"mocked response"
                        mock_post.return_value.headers = {"content-type": "text/plain"}
                        mock_client_instance.__aenter__.return_value.post = mock_post

                        mock_client_instance2 = MockClient2.return_value
                        mock_post2 = AsyncMock()
                        mock_post2.return_value.content = b"mocked response"
                        mock_post2.return_value.headers = {"content-type": "text/plain"}
                        mock_client_instance2.__aenter__.return_value.post = mock_post

                        # Prepare the request payload with the necessary 'nodes' key
                        payload = {"filename": "file1", "content": '{"content"}'}

                        async with await anyio.open_file("file1.zip", "w") as f:
                            await f.write("")

                        # Send the request to the endpoint
                        response = client.post("/convert", json=payload)
                        # Validate the response

                        assert response.status_code == 200
                        assert response.headers["content-type"] == "application/zip"
                        mock_remove.assert_called()

                        os.remove("file1.zip")
