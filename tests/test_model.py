import pytest
from pydantic import ValidationError

from app.main import (
    DownloadRequest,
)  # Update this import if the model is in another file


def test_valid_download_request():
    """Test that a valid DownloadRequest model works correctly."""
    data = {"filename": "example", "content": "Hello, world!"}
    request = DownloadRequest(**data)

    assert request.filename == "example"
    assert request.content == "Hello, world!"


def test_missing_filename():
    """Test that missing filename raises a ValidationError."""
    data = {"content": "Hello, world!"}  # No filename
    with pytest.raises(ValidationError):
        DownloadRequest(**data)


def test_missing_content():
    """Test that missing content raises a ValidationError."""
    data = {"filename": "example"}  # No content
    with pytest.raises(ValidationError):
        DownloadRequest(**data)


def test_empty_filename():
    """Test that an empty filename raises a ValidationError."""
    data = {"filename": "", "content": "Some content"}
    with pytest.raises(ValidationError):
        DownloadRequest(**data)


def test_empty_content():
    """Test that an empty content field is allowed."""
    data = {"filename": "example", "content": ""}
    request = DownloadRequest(**data)

    assert request.filename == "example"
    assert request.content == ""  # Empty content is valid
