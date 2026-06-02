from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from idkollen_client.models.document import DocumentUploadResponse

if TYPE_CHECKING:
    from idkollen_client._client import IdkollenClient, AsyncIdkollenClient

_upload_adapter: TypeAdapter[DocumentUploadResponse] = TypeAdapter(DocumentUploadResponse)


class DocumentEndpoint:
    def __init__(self, client: "IdkollenClient") -> None:
        self._client = client

    def upload(self, data: bytes, filename: str, mime_type: str = "application/pdf") -> DocumentUploadResponse:
        files = {"file": (filename, data, mime_type)}
        return self._client._post_multipart("/document", files, _upload_adapter)

    def download(self, id: str) -> bytes:
        return self._client._get_bytes(f"/document/{id}")

    def delete(self, id: str) -> None:
        return self._client._delete(f"/document/{id}")


class AsyncDocumentEndpoint:
    def __init__(self, client: "AsyncIdkollenClient") -> None:
        self._client = client

    async def upload(self, data: bytes, filename: str, mime_type: str = "application/pdf") -> DocumentUploadResponse:
        files = {"file": (filename, data, mime_type)}
        return await self._client._post_multipart("/document", files, _upload_adapter)

    async def download(self, id: str) -> bytes:
        return await self._client._get_bytes(f"/document/{id}")

    async def delete(self, id: str) -> None:
        return await self._client._delete(f"/document/{id}")
