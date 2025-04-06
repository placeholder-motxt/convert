import os
from unittest.mock import MagicMock, Mock, patch

import anyio
import pytest
from fastapi.testclient import TestClient

from app.main import app, check_duplicate
from app.models.elements import ClassObject, ModelsElements
from app.models.methods import ClassMethodObject

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
            patch("app.main.fetch_data") as mock_fetch_data,
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

            mock_fetch_data.return_value = {
                "models": "class Test {}",
                "views": "view Test {}",
                "model_element": ModelsElements("filename"),
            }

            # Try to upload a file
            response = client.post(
                "/convert/",
                json={"filename": ["file1"], "content": [['{"Some content":"a"}']]},
            )
            assert response.status_code == 400
            assert response.json()["detail"] == "Please try again later"
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
        patch("app.main.fetch_data") as mock_fetch_data,
    ):
        mockjson.loads.return_value = {"diagram": "ClassDiagram"}

        mock_instance = mockparser.return_value
        mock_instance.parse.return_value = [MagicMock()]
        mock_instance.print_django_style.return_value = "ini class write"

        mock_instance2 = mockparser2.return_value
        mock_instance2.add_class_method.return_value = [MagicMock()]

        mock_fetch_data.return_value = {
            "models": "class Test {}",
            "views": "view Test {}",
            "model_element": ModelsElements("filename"),
        }

        response = client.post(
            "/convert/", json={"filename": ["app/main2"], "content": [["Some content"]]}
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "/ not allowed in file name"


@pytest.mark.asyncio
async def test_convert_endpoint_valid_content_class_diagram():
    # Mock ParseJsonToObjectClass to avoid executing its real implementation
    with (
        patch("app.main.ModelsElements") as mockparser,
        patch("app.main.ViewsElements") as mockparser2,
        patch("app.main.json") as mockjson,
        patch("app.main.fetch_data") as mock_fetch_data,
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

        mock_fetch_data.return_value = {
            "models": "class Test {}",
            "views": "view Test {}",
            "model_element": ModelsElements("filename"),
        }

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
async def test_convert_endpoint_inconsistent_filename_content_length():
    payload = {
        "filename": ["file1", "file2"],  # Two filenames
        "content": [['{"diagram": "ClassDiagram"}']],  # Only one content
    }

    # Assuming `client` is initialized somewhere like this:
    client = TestClient(app)

    response = client.post("/convert", json=payload)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "number of Filename and Content is incosistent"
    }


@pytest.mark.asyncio
async def test_convert_endpoint_class_diagram():
    # Mock `ModelsElements` and `ViewsElements`
    with (
        patch("app.main.ModelsElements") as mock_models,
        patch("app.main.ViewsElements") as mock_views,
        patch("app.main.json") as mock_json,
        patch("app.main.fetch_data") as mock_fetch_data,
    ):
        mock_json.loads.return_value = {"diagram": "ClassDiagram"}
        mock_instance_models = mock_models.return_value
        mock_class = MagicMock()
        mock_class.get_methods.return_value = [MagicMock(to_views_code="view Test {}")]
        mock_instance_models.parse.return_value = [mock_class]
        mock_instance_models.print_django_style.return_value = "ini class write"

        mock_instance_views = mock_views.return_value
        mock_instance_views.add_class_method.return_value = MagicMock()
        mock_instance_views.print_django_style.return_value = "ini views write"

        mock_fetch_data.return_value = {
            "models": "class Test {}",
            "views": "view Test {}",
            "model_element": ModelsElements("filename"),
        }

        payload = {"filename": ["file1"], "content": [['{"diagram": "ClassDiagram"}']]}

        client = TestClient(app)

        response = client.post("/convert", json=payload)

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/zip"
        assert response.content.startswith(
            b"PK"
        )  # Check that the response is a zip file


@pytest.mark.asyncio
async def test_convert_endpoint_sequence_diagram():
    # Mock `ParseJsonToObjectSeq`, `ModelsElements`, `ViewsElements`, and `check_duplicate`
    with (
        patch("app.main.ParseJsonToObjectSeq") as mock_seq_parser,
        patch("app.main.ModelsElements") as mock_models,
        patch("app.main.ViewsElements") as mock_views,
        patch("app.main.fetch_data") as mock_fetch_data,  # Mock fetch data
    ):
        # Set up mock for sequence diagram parsing
        mock_seq_instance = mock_seq_parser.return_value
        mock_seq_instance.set_json.return_value = None
        mock_seq_instance.parse.return_value = None
        mock_seq_instance.parse_return_edge.return_value = None
        mock_seq_instance.get_controller_method.return_value = [MagicMock()]
        mock_seq_instance.get_class_objects.return_value = [MagicMock()]

        # Mock `ModelsElements` to return valid data
        mock_instance_models = mock_models.return_value
        mock_class = MagicMock()
        mock_method = MagicMock()
        mock_method.get_name.return_value = "method_name"
        mock_class.get_methods.return_value = [mock_method]
        mock_instance_models.parse.return_value = [mock_class]

        # Ensure `print_django_style` returns valid strings
        mock_instance_models.print_django_style.return_value = "ini class write"

        # Mock `ViewsElements` to behave as expected
        mock_instance_views = mock_views.return_value
        mock_instance_views.print_django_style.return_value = "ini views write"

        mock_fetch_data.return_value = {
            "models": "class Test {}",
            "views": "view Test {}",
            "model_element": ModelsElements("filename"),
        }

        # Prepare the payload
        payload = {
            "filename": ["file1"],
            "content": [['{"diagram": "SequenceDiagram"}']],
        }

        # Send the request to the endpoint
        client = TestClient(app)

        response = client.post("/convert", json=payload)

        # Validate that fetch_data was called
        mock_fetch_data.assert_called()  # Check that the function was called

        # Validate the response
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/zip"
        assert response.content.startswith(
            b"PK"
        )  # Check that the response is a zip file


@pytest.mark.asyncio
async def test_convert_endpoint_invalid_diagram_type():
    # Mock `ModelsElements` and `ViewsElements`
    with (
        patch("app.main.ModelsElements") as mock_models,
        patch("app.main.ViewsElements") as mock_views,
        patch("app.main.json") as mock_json,
        patch("app.main.fetch_data") as mock_fetch_data,
    ):
        mock_json.loads.return_value = {"diagram": "InvalidDiagram"}
        mock_instance_models = mock_models.return_value
        mock_instance_models.parse.return_value = []
        mock_instance_models.print_django_style.return_value = "ini class write"

        mock_instance_views = mock_views.return_value
        mock_instance_views.print_django_style.return_value = "ini views write"

        mock_fetch_data.return_value = {
            "models": "class Test {}",
            "views": "view Test {}",
            "model_element": ModelsElements("filename"),
        }

        payload = {
            "filename": ["file1"],
            "content": [['{"diagram": "InvalidDiagram"}']],
        }

        # Assuming `client` is initialized somewhere like this:
        client = TestClient(app)

        response = client.post("/convert", json=payload)

        assert (
            response.status_code == 200
        )  # assuming it doesn't throw an error and just skips
        # invalid diagrams


@pytest.mark.asyncio
async def test_convert_endpoint_valid_sequence_diagram():
    payload = {
        "filename": ["simple.class.jet", "simple.sequence.jet"],
        "content": [
            [
                '{"diagram":"ClassDiagram", "nodes":[{"methods":"classMethod()", "name":"Test", '
                '"x":100, "y":100}], "edges":[]}'
            ],
            [
                '{"diagram":"SequenceDiagram", "nodes":[{"children":[1], "name":":UI", "x":80,'
                ' "y":5, "id":0, "type":"ImplicitParameterNode"}], "edges":[{"middleLabel":"doA ()"'
                ', "start":1, "end":3, "type":"CallEdge"}]}'
            ],
        ],
    }

    with (
        patch("app.main.ParseJsonToObjectSeq") as mockseq,
        patch("app.main.ViewsElements") as mockparser2,
        patch("app.main.json") as mockjson,
        patch("app.main.check_duplicate") as mock_check_duplicate,
        patch("app.main.generate_create_page_views", return_value="create views code"),
        patch("app.main.generate_edit_page_views", return_value="edit views code"),
        patch("app.main.generate_delete_page_views", return_value="delete views code"),
        patch("app.main.generate_read_page_views", return_value="read views code"),
        patch(
            "app.main.generate_landing_page_views", return_value="landing views code"
        ),
    ):
        mockjson.loads.return_value = {"diagram": "SequenceDiagram"}

        seq_parser = mockseq.return_value
        seq_parser.get_controller_method.return_value = [MagicMock()]
        seq_parser.get_class_objects.return_value = [MagicMock()]

        mock_instance2 = mockparser2.return_value
        mock_instance2.add_class_method.return_value = [MagicMock()]
        mock_instance2.print_django_style.return_value = "views code"

        response = client.post("/convert", json=payload)
        mock_check_duplicate.assert_called()
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/zip"


@pytest.mark.asyncio
async def test_convert_endpoint_valid_multiple_file_content():
    # Mock ParseJsonToObjectClass to avoid executing its real implementation
    with (
        patch("app.main.ModelsElements") as mockparser,
        patch("app.main.ViewsElements") as mockparser2,
        patch("app.main.json") as mockjson,
        patch("app.main.fetch_data") as mock_fetch_data,
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
        mock_fetch_data.return_value = {
            "models": "class Test {}",
            "views": "view Test {}",
            "model_element": ModelsElements("filename"),
        }

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


def test_check_duplicate_class_object_not_in_class_objects():
    # Mocking class objects and class method objects
    class_objects = {}  # Empty class_objects dictionary
    class_object = Mock()  # Mocked class object
    class_object.get_name.return_value = "class1"
    duplicate_class_method_checker = {}

    result = check_duplicate(
        class_objects, class_object.get_name(), duplicate_class_method_checker
    )

    # Assert that duplicate_class_method_checker remains unchanged
    assert result == duplicate_class_method_checker


def test_check_duplicate_no_matching_method():
    # class_objects with a class_object and methods, but empty duplicate_class_method_checker
    class_method_object = Mock()
    class_method_object.get_name.return_value = "method1"

    class_object = ClassObject()
    class_object.add_method(class_method_object)
    class_object.set_name("class1")

    # Creating a mock for class_objects to behave like a dictionary with the right behavior
    class_objects = {class_object.get_name(): class_object}
    duplicate_class_method_checker = {"hello": ClassObject()}
    with pytest.raises(
        ValueError,
        match="Cannot call class 'class1' objects not defined in Class Diagram!",
    ):
        check_duplicate(
            class_objects, class_object.get_name(), duplicate_class_method_checker
        )


def test_check_duplicate_with_matching_method():
    # Mocking class objects and class method objects
    class_method_object = ClassMethodObject()
    class_method_object.set_name("method1")

    class_method_object_copy = ClassMethodObject()
    class_method_object_copy.set_name("method1")

    class_object = ClassObject()
    class_object.add_method(class_method_object)

    # Create class_objects dictionary that returns a mock object for class_object
    class_objects = {class_object.get_name(): class_object}

    # Initialize duplicate_class_method_checker with a method already present
    duplicate_class_method_checker = {
        (class_object.get_name(), class_method_object.get_name()): class_method_object
    }

    # Run the check_duplicate function
    result = check_duplicate(
        class_objects, class_object.get_name(), duplicate_class_method_checker
    )

    # Assert that the method `method2` has been added/updated in duplicate_class_method_checker
    assert len(result) == 1
    assert (class_object.get_name(), "method1") in result
    assert result[(class_object.get_name(), "method1")] == class_method_object_copy


def test_check_duplicate_empty_class_objects_and_methods():
    # Empty class_objects and duplicate_class_method_checker
    class_objects = {}
    class_object = ClassObject()
    class_object.set_name("class1")
    duplicate_class_method_checker = {}

    result = check_duplicate(
        class_objects, class_object.get_name(), duplicate_class_method_checker
    )

    # Assert that the result remains the same since there are no class objects or methods to check
    assert result == duplicate_class_method_checker


def test_check_duplicate_empty_duplicate_class_method_checker():
    # class_objects with a class_object and methods, but empty duplicate_class_method_checker
    class_method_object = Mock()
    class_method_object.get_name.return_value = "method1"

    class_object = ClassObject()
    class_object.add_method(class_method_object)
    class_object.set_name("class1")

    # Creating a mock for class_objects to behave like a dictionary with the right behavior
    class_objects = {class_object.get_name(): class_object}
    duplicate_class_method_checker = {}

    with pytest.raises(
        ValueError,
        match="Cannot call class 'class1' objects not defined in Class Diagram!",
    ):
        check_duplicate(
            class_objects, class_object.get_name(), duplicate_class_method_checker
        )


def test_raise_value_error_on_main():
    payload = {
        "filename": ["file1.sequence,jet"],
        "content": [['{"diagram": "SequenceDiagram"}']],
    }
    response = client.post("/convert", json=payload)
    assert response.status_code == 422
    assert response.json() == {
        "detail": "The .sequence.jet is not valid. \n"
        "Please make sure the file submitted is not corrupt"
    }
    app.dependency_overrides.clear()  # Reset overrides after test
