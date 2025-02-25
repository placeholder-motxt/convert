from fastapi.testclient import TestClient
from app.main import app
import pytest
import os

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI World!"}

@pytest.fixture
def test_file():
    """Provides a test file name and content"""
    return {
        "filename": "testfile",
        "content": "print('Hello, world!')"
    }

def test_download_file(test_file):
    """Test the /download/ endpoint"""

    response = client.post("/download/", json=test_file)

    assert response.status_code == 200

    downloaded_content = response.content.decode("utf-8")
    assert downloaded_content == test_file["content"]

    file_path = test_file["filename"] + ".py"
    assert not os.path.exists(file_path)