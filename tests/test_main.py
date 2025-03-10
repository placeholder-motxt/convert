import os
from unittest.mock import MagicMock, patch

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
    with open("file1_models.py", "w") as f:
        f.write("Some initial content")

    try:
        with (
            patch("app.main.ModelsElements") as mockparser,
            patch("app.main.ViewsElements") as mockparser2,
            patch("app.main.json") as mockjson,
        ):
            mockjson.loads.return_value = {"diagram": "ClassDiagram"}
            mock_instance = mockparser.return_value
            mock_instance.parse.return_value = [
                MagicMock(to_models_code=MagicMock(return_value="class Test {}"))
            ]

            mockjson.return_value = {}

            mock_instance.print_django_style.return_value = "ini class write"

            mock_instance2 = mockparser2.return_value
            mock_instance2.add_class_method.return_value = [
                MagicMock(to_views_code=MagicMock(return_value="view Test {}"))
            ]
            mock_instance2.print_django_style.return_value = "ini views write"

            # Try to upload a file
            response = client.post(
                "/convert/",
                json={"filename": ["file1"], "content": [['{"Some content":"a"}']]},
            )
            assert response.status_code == 400
            assert response.json()["detail"] == "The file already exists."
    finally:
        # Clean up: remove the file created for the test
        if os.path.exists("file1_models.py"):
            os.remove("file1_models.py")


def test_slash_on_filename():
    # Try to upload a file
    with (
        patch("app.main.ModelsElements") as mockparser,
        patch("app.main.ViewsElements") as mockparser2,
        patch("app.main.json") as mockjson,
    ):
        mockjson.loads.return_value = {"diagram": "ClassDiagram"}

        mock_instance = mockparser.return_value
        mock_instance.parse.return_value = [MagicMock()]
        mock_instance.print_django_style.return_value = "ini class write"

        mock_instance2 = mockparser2.return_value
        mock_instance2.add_class_method.return_value = [MagicMock()]

        response = client.post(
            "/convert/", json={"filename": ["app/main2"], "content": [["Some content"]]}
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "/ not allowed"


@pytest.mark.asyncio
async def test_convert_endpoint_valid_content_class_diagram():
    # Mock ParseJsonToObjectClass to avoid executing its real implementation
    with (
        patch("app.main.ModelsElements") as mockparser,
        patch("app.main.ViewsElements") as mockparser2,
        patch("app.main.json") as mockjson,
    ):
        mockjson.loads.return_value = {"diagram": "ClassDiagram"}
        mock_instance = mockparser.return_value
        m = MagicMock()
        m.get_methods.return_value = [MagicMock(to_views_code="view Test {}")]
        mock_instance.parse.return_value = [m]
        mock_instance.print_django_style.return_value = "ini class write"

        mock_instance2 = mockparser2.return_value
        mock_instance2.add_class_method.return_value = [MagicMock()]
        mock_instance2.print_django_style.return_value = "ini views write"

        # Prepare the request payload with the necessary 'nodes' key
        payload = {"filename": ["file1"], "content": [['{"content"}']]}

        async with await anyio.open_file("file1.zip", "w") as f:
            await f.write("")

        # Send the request to the endpoint
        response = client.post("/convert", json=payload)
        # Validate the response

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/zip"

@pytest.mark.asyncio
async def test_convert_endpoint_valid_sequence_diagram():
        payload = {"filename": ["simple.class.jet", "simple.sequence.jet"],
                   "content": [[('{"diagram":"ClassDiagram",'
                   '"nodes":[{"methods":"- classMethod (): void","name":"ClassName",'
                   '"x":390,"y":80,"attributes":"","id":0,"type":"ClassNode"}],"edges":[],"version":"3.8"}')],
                   [('{"diagram":"SequenceDiagram","nodes":[{"children":[1],"name":":UI",'
                   '"x":80,"y":58,"id":0,"type":"ImplicitParameterNode"},'
                   '{"x":0,"y":0,"openBottom":false,"id":1,"type":"CallNode"},'
                   '{"children":[3],"name":":views","x":450,"y":50,"id":2,'
                   '"type":"ImplicitParameterNode"},{"x":0,"y":0,"openBottom":false,"id":3,'
                   '"type":"CallNode"},{"children":[5],"name":"class_name:ClassName","x":730,'
                   '"y":60,"id":4,"type":"ImplicitParameterNode"},{"x":0,"y":0,"openBottom":false,'
                   '"id":5,"type":"CallNode"}],"edges":[{"middleLabel":"doA ()","start":1,"end":3,'
                   '"type":"CallEdge","signal":false},{"middleLabel":"classMethod ()","start":3,'
                   '"end":5,"type":"CallEdge","signal":false},{"middleLabel":"return_var","start":5,"end":3,"type":"ReturnEdge"}],"version":"3.8"}')]]}
        response = client.post("/convert", json=payload)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/zip"

        # mock_instance2.add_class_method.assert_called()

@pytest.mark.asyncio
async def test_convert_endpoint_valid_multiple_file_content():
    # Mock ParseJsonToObjectClass to avoid executing its real implementation
    with (
        patch("app.main.ModelsElements") as mockparser,
        patch("app.main.ViewsElements") as mockparser2,
        patch("app.main.json") as mockjson,
    ):
        mockjson.loads.return_value = {"diagram": "ClassDiagram"}
        mock_instance = mockparser.return_value
        m = MagicMock()
        mock_instance.parse.return_value = [m, m, m]
        mock_instance.print_django_style.return_value = "ini class write"
        m.get_methods.return_value = [MagicMock(to_views_code="view Test {}")]

        mock_instance2 = mockparser2.return_value
        mock_instance2.add_class_method.return_value = None
        mock_instance2.print_django_style.return_value = "ini views write"

        payload = {
            "filename": ["file1", "file2"],
            "content": [['{"content"}'], ['{"content"}']],
        }
        response = client.post("/convert", json=payload)

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/zip"


@pytest.mark.asyncio
async def test_convert_endpoint_invalid_incosistent_filename_content_amount():
    payload = {"filename": ["file1"], "content": [['{"content"}'], ['{"content"}']]}
    response = client.post("/convert", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "number of Filename and Content is incosistent"
