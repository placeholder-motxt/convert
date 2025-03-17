import pytest
from pydantic import ValidationError

from app.main import ConvertRequest, DownloadRequest


def test_valid_download_request():
    """Test that a valid DownloadRequest model works correctly."""
    data = {"filename": "example", "content": "Hello, world!", "type": "models"}
    request = DownloadRequest(**data)

    assert request.filename == "example"
    assert request.content == "Hello, world!"
    assert request.type == "models"


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


def test_invalid_short_filename():
    """Test that an empty filename raises a ValidationError."""
    data = {"filename": "12", "content": "Some content"}
    with pytest.raises(ValidationError):
        DownloadRequest(**data)


def test_empty_content():
    """Test that an empty content field is allowed."""
    data = {"filename": "example", "content": ""}
    request = DownloadRequest(**data)

    assert request.filename == "example"
    assert request.content == ""  # Empty content is valid


def test_empty_type():
    """Test that an empty type is allowed."""
    data = {"filename": "filename", "content": "", "type": ""}
    request = DownloadRequest(**data)

    assert request.type == ""


def test_valid_convert_request():
    """Test that a valid DownloadRequest model works correctly."""
    data = {
        "filename": ["example1", "example2"],
        "content": [["Hello, world!"], ["Hello, world!2"]],
    }
    request = ConvertRequest(**data)

    assert request.filename == ["example1", "example2"]
    assert request.content == [["Hello, world!"], ["Hello, world!2"]]


def test_empty_content_convert():
    """Test that missing content raises a ValidationError."""
    data = {"filename": ["1", "2"], "content": []}
    with pytest.raises(ValidationError):
        ConvertRequest(**data)


def test_empty_filename_content_convert():
    """Test that missing content raises a ValidationError."""
    data = {"filename": [], "content": [[]]}
    with pytest.raises(ValidationError):
        ConvertRequest(**data)
