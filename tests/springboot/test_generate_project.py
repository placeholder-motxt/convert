import asyncio
import os
import tempfile
import zipfile
from unittest.mock import AsyncMock, MagicMock, patch

import anyio
from pytest import fixture
from pytest_bdd import given, scenarios, then, when

from app.main import convert_spring

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FEATURE_PATH = os.path.join(
    BASE_DIR, "..", "features", "springboot", "generate_project.feature"
)

scenarios(FEATURE_PATH)


@fixture
def context() -> dict:
    return {}


@given("the parsed class diagram project name and group id")
def prepare_context(context: dict):
    asyncio.run(_prepare_context(context))


async def _prepare_context(context: dict):
    with patch("httpx.AsyncClient") as mock_client_class:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "application/zip"}

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip:
            with zipfile.ZipFile(tmp_zip.name, "w") as zipf:
                zipf.writestr("src/main/java/", "")
                zipf.writestr("src/test/java/", "")
                zipf.writestr("build.gradle.kts", "")
                zipf.writestr("src/main/resources/application.properties", "abcd=abcd")

            async with await anyio.open_file(tmp_zip.name, "rb") as f:
                mock_response.content = await f.read()

            context["mock_zip_path"] = tmp_zip.name

        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance

        data = {
            "project_name": "iniGacor",
            "group_id": "com.example",
            "project_type": "spring",
            "filename": ["Dummy Dat_1.class.jet"],
            "content": [
                [
                    '{"diagram":"ClassDiagram","nodes":['
                    '{"methods":"","name":"+ Shape","x":100,"y":70,"attributes":"+ colour: string"'
                    ',"id":0,"type":"ClassNode"},{"methods":"+ getId (): string\\n+ setRadius '
                    '(radius: integer): void","name":"+ Circle","x":320,"y":70,"attributes":'
                    '"- radius: integer\\n- id: string","id":1,"type":"ClassNode"},{"methods":'
                    '"+ findCircle(circleid: string): string","name":"+ Circles","x":190,"y":'
                    '300,"attributes":"","id":2,"type":"ClassNode"}],"edges":[{"Generalization '
                    'Type":"Inheritance","start":1,"end":0,"type":"GeneralizationEdge"},'
                    '{"startLabel":"*","middleLabel":"","start":1,"directionality":"Unspecified","end":2,"endLabel":"1","type":"AssociationEdge"}'
                    '],"version":"3.8"}'
                ]
            ],
        }

        context["project_name"] = data["project_name"]
        context["group_id"] = data["group_id"]

        zip_path = await convert_spring(
            project_name=data["project_name"],
            group_id=data["group_id"],
            filenames=data["filename"],
            contents=data["content"],
        )

        context["result_zip_path"] = zip_path


@when("the zip is unzip")
def unzip_result(context: dict):
    with zipfile.ZipFile(context["result_zip_path"], "r") as zip_ref:
        context["file_list"] = zip_ref.namelist()
        context["src_path"] = (
            f"src/main/java/{context['group_id'].replace('.', '/')}/{context['project_name']}"
        )

        if "application.properties" in context["file_list"]:
            context["application_properties"] = zip_ref.read(
                "application.properties"
            ).decode("utf-8")


@then("the zip contains model folder that consists of all models")
def check_model_folder(context: dict):
    for model in ["Shape", "Circle", "Circles"]:
        assert f"{context['src_path']}/model/{model}.java" in context["file_list"]


@then("the zip contains repository folder for all models")
def check_repository_folder(context: dict):
    print("aaaa", context["file_list"])
    for model in ["ShapeRepository", "CircleRepository", "CirclesRepository"]:
        assert f"{context['src_path']}/repository/{model}.java" in context["file_list"]


@then("the zip contains service folder for all models")
def check_service_folder(context: dict):
    for model in ["ShapeService", "CircleService", "CirclesService"]:
        assert f"{context['src_path']}/service/{model}.java" in context["file_list"]


@then("the zip contains controller folder for all models")
def check_controller_folder(context: dict):
    for model in [
        "ShapeController",
        "CircleController",
        "CirclesController",
        "HomeController",
    ]:
        assert f"{context['src_path']}/controller/{model}.java" in context["file_list"]


@then("the zip contains application.properties")
def check_application_properties(context: dict):
    assert "src/main/resources/application.properties" in context["file_list"]


@given("the context JSON with no diagram type")
def prepare_invalid_jet_content(context: dict):
    context["data"] = {
        "project_name": "invalidProj",
        "group_id": "com.test",
        "project_type": "spring",
        "filename": ["Invalid_1.class.jet"],
        "content": [
            [
                '{"nodes":[{"methods":"","name":"Shape","x":100,"y":70,"attributes":"+ colour: '
                'string","id":0,"type":"ClassNode"},{"methods":"+ getId (): string\\n+ setRadius '
                '(radius: integer): void","name":"Circle","x":320,"y":70,"attributes":"- radius: '
                'integer\\n- id: string","id":1,"type":"ClassNode"},{"methods":"+ findCircle('
                'circleid: string): string","name":"Circles","x":190,"y":300,"attributes":"",'
                '"id":2,'
                '"type":"ClassNode"}],"edges":[{"Generalization Type":"Inheritance",'
                '"start":1,"end":0,"type":"GeneralizationEdge"},{"startLabel":"*","middleLabel":'
                '"","start":1,"directionality":"Unspecified","end":2,"endLabel":"1","type":"AssociationEdge"}'
                '],"version":"3.8"}'
            ]
        ],
    }


@when("the content is parsed")
def prepare_content(context: dict):
    try:
        asyncio.run(call_convert_spring(context))
    except Exception as e:
        context["exception"] = e


async def call_convert_spring(context: dict):
    with patch("httpx.AsyncClient") as mock_client_class:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "application/zip"}

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip:
            with zipfile.ZipFile(tmp_zip.name, "w") as zipf:
                zipf.writestr("src/main/java/", "")
                zipf.writestr("src/test/java/", "")

            async with await anyio.open_file(tmp_zip.name, "rb") as f:
                mock_response.content = await f.read()

            context["mock_zip_path"] = tmp_zip.name

        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance

        data = context["data"]

        context["project_name"] = data["project_name"]
        context["group_id"] = data["group_id"]

        zip_path = await convert_spring(
            project_name=data["project_name"],
            group_id=data["group_id"],
            filenames=data["filename"],
            contents=data["content"],
        )

        context["result_zip_path"] = zip_path
        data = context["data"]
        context["exception"] = None
        asyncio.run(
            convert_spring(
                project_name=data["project_name"],
                group_id=data["group_id"],
                filenames=data["filename"],
                contents=data["content"],
            )
        )


@then("program will raise error for no diagram")
def check_error(context: dict):
    assert context["exception"] is not None, "Expected exception, but none was raised"
    assert isinstance(context["exception"], ValueError)
    assert str(context["exception"]) == "Diagram type not found on .jet file"


@given("the context JSON with invalid diagram")
def prepare_invalid_diagram(context: dict):
    context["data2"] = {
        "project_name": "invalidProj",
        "group_id": "com.test",
        "project_type": "spring",
        "filename": ["Invalid_1.class.jet"],
        "content": [
            [
                '{"diagram":"Diagram","nodes":[{"methods":"","name":"Shape","x":100,"y":70,'
                '"attributes":"+ colour: string","id":0,"type":"ClassNode"},{"methods":'
                '"+ getId (): string\\n+ setRadius (radius: integer): void","name":"Circle","x":'
                '320,"y":70,"attributes":"- radius: integer\\n- id: string","id":1,"type":'
                '"ClassNode"},{"methods":"+ findCircle(circleid: string): string","name":"Circles",'
                '"x":190,"y":300,"attributes":"","id":2,"type":"ClassNode"}],"edges":[{"'
                'Generalization Type":"Inheritance","start":1,"end":0,"type":"GeneralizationEdge"},'
                '{"startLabel":"*","middleLabel":"","start":1,"directionality":"Unspecified","end":2,"endLabel":"1","type":"AssociationEdge"}'
                '],"version":"3.8"}\r\n'
            ]
        ],
    }


@when("content is parsed")
def prepare_content2(context: dict):
    try:
        asyncio.run(call_convert_spring2(context))
    except Exception as e:
        context["exception2"] = e


async def call_convert_spring2(context: dict):
    with patch("httpx.AsyncClient") as mock_client_class:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "application/zip"}

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip:
            with zipfile.ZipFile(tmp_zip.name, "w") as zipf:
                zipf.writestr("src/main/java/", "")
                zipf.writestr("src/test/java/", "")

            async with await anyio.open_file(tmp_zip.name, "rb") as f:
                mock_response.content = await f.read()

            context["mock_zip_path2"] = tmp_zip.name

        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance

        data = context["data2"]

        zip_path = await convert_spring(
            project_name=data["project_name"],
            group_id=data["group_id"],
            filenames=data["filename"],
            contents=data["content"],
        )

        context["result_zip_path2"] = zip_path
        data = context["data2"]
        context["exception2"] = None
        asyncio.run(
            convert_spring(
                project_name=data["project_name"],
                group_id=data["group_id"],
                filenames=data["filename"],
                contents=data["content"],
            )
        )


@then("program will raise error for invalid diagram")
def check_error_2(context: dict):
    assert context["exception2"] is not None, "Expected exception, but none was raised"
    assert isinstance(context["exception2"], ValueError)
    assert str(context["exception2"]) == "Unknown diagram type. Diagram type must be ClassDiagram or SequenceDiagram"


def cleanup(context: dict):
    if "result_zip_path" in context and os.path.exists(context["result_zip_path"]):
        os.unlink(context["result_zip_path"])
    if "mock_zip_path" in context and os.path.exists(context["mock_zip_path"]):
        os.unlink(context["mock_zip_path"])
