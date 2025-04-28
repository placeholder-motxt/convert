import os
import unittest
from unittest.mock import AsyncMock, patch

import anyio
import httpx
from fastapi import HTTPException

from app.config import SPRING_DEPENDENCIES
from app.main import initialize_springboot_zip


class TestInitializeSpringZip(unittest.IsolatedAsyncioTestCase):
    @patch("app.main.httpx.AsyncClient.get")
    async def test_successful_download_with_zip_content(self, mock_get: AsyncMock):
        """Test successful download with zip content returns tempfile path"""
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "application/zip"}
        mock_response.content = b"PK\x03\x04"

        mock_get.return_value = mock_response
        temp_file_path = await initialize_springboot_zip("testing", "com.motxt")

        params = {
            "javaVersion": "21",
            "artifactId": "testing",
            "groupId": "com.motxt",
            "name": "testing",
            "packaging": "jar",
            "type": "gradle-project-kotlin",
            "dependencies": SPRING_DEPENDENCIES,
        }
        mock_get.assert_called_once_with("http://localhost:8080/starter.zip", params=params)
        self.assertTrue(temp_file_path.endswith(".zip"))
        # Verify file exists and has content
        async with await anyio.open_file(temp_file_path, "rb") as f:
            self.assertEqual(await f.read(), b"PK\x03\x04")

        os.remove(temp_file_path)

    @patch("app.main.httpx.AsyncClient.get")
    async def test_non_200_status_raises_exception(self, mock_get: AsyncMock):
        """Test non-200 status code raises HTTPException"""
        mock_response = AsyncMock()
        mock_response.status_code = 500

        mock_get.return_value = mock_response
        with self.assertRaises(HTTPException) as ctx:
            await initialize_springboot_zip("testing", "com.motxt")

        self.assertEqual(
            str(ctx.exception),
            "500: Unknown error occured. Initializr service might be down.",
        )

    @patch("app.main.httpx.AsyncClient.get")
    async def test_non_zip_content_raises_exception(self, mock_get: AsyncMock):
        """Test non-zip content type raises HTTPException"""
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "text/html"}

        mock_get.return_value = mock_response

        with self.assertRaises(HTTPException) as ctx:
            await initialize_springboot_zip("testing", "com.motxt")

        self.assertEqual(
            str(ctx.exception), "500: Unexpected content type from server: text/html."
        )

    @patch("app.main.httpx.AsyncClient.get")
    async def test_timeout_raises_exception(self, mock_get: AsyncMock):
        """Test timeout raises HTTPException"""
        mock_get.side_effect = httpx.TimeoutException("Timeout")
        with self.assertRaises(HTTPException) as ctx:
            await initialize_springboot_zip("testing", "com.motxt")

        self.assertEqual(
            str(ctx.exception),
            "503: Initializr service timed out. Please try again later.",
        )

    @patch("app.main.httpx.AsyncClient.get")
    async def test_connection_error_raises_exception(self, mock_get: AsyncMock):
        """Test connection error raises HTTPException"""
        mock_get.side_effect = httpx.NetworkError("Connection error")
        with self.assertRaises(HTTPException) as ctx:
            await initialize_springboot_zip("testing", "com.motxt")

        self.assertEqual(
            str(ctx.exception),
            "503: Cannot connect to Initializr service. Service might be down.",
        )

    @patch("app.main.httpx.AsyncClient.get")
    async def test_empty_response_raises_exception(self, mock_get: AsyncMock):
        """Test empty response raises HTTPException"""
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "application/zip"}
        mock_response.content = b""

        mock_get.return_value = mock_response

        with self.assertRaises(HTTPException) as ctx:
            await initialize_springboot_zip("testing", "com.motxt")

        self.assertEqual(
            str(ctx.exception), "500: Failed to create zip, please try again later."
        )

    @patch("app.main.httpx.AsyncClient.get")
    async def test_large_zip_file_handled_properly(self, mock_get: AsyncMock):
        """Test large zip file is handled correctly"""
        large_content = b"0" * (1024 * 1024)  # 1MB of data

        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "application/zip"}
        mock_response.content = large_content

        mock_get.return_value = mock_response

        temp_file_path = await initialize_springboot_zip("testing", "com.motxt")

        async with await anyio.open_file(temp_file_path, "rb") as f:
            self.assertEqual(len(await f.read()), len(large_content))

        os.remove(temp_file_path)
