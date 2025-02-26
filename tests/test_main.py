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

def test_file_already_exists():
    with open("a.py", "w") as f:
        f.write("Some initial content")
        
    try:
        # Try to upload a file
        response = client.post("/download/", json={"filename":"a","content": "Some content"})
        assert response.status_code, 400
        assert response.json()["detail"], "The file already exists."
    finally:
        # Clean up: remove the file created for the test
        if os.path.exists("a.py"):
            os.remove("a.py")

def test_slash_on_filename():
    # Try to upload a file
    response = client.post("/download/", json={"filename":"app/main2","content": "Some content"})
    assert response.status_code==400
    assert response.json()["detail"]=="/ not allowed"
