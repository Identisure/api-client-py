from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from identisure_client.models.document import DocumentUploadResponse

if TYPE_CHECKING:
    from identisure_client._client import IdentisureClient, AsyncIdentisureClient

_upload_adapter: TypeAdapter[DocumentUploadResponse] = TypeAdapter(DocumentUploadResponse)


class DocumentEndpoint:
    def __init__(self, client: "IdentisureClient") -> None:
        self._client = client

    def upload(self, data: bytes, filename: str, mime_type: str = "application/pdf") -> DocumentUploadResponse:
        files = {"file": (filename, data, mime_type)}
        return self._client._post_multipart("/v3/document", files, _upload_adapter)

    def download(self, id: str) -> bytes:
        return self._client._get_bytes(f"/v3/document/{id}")


class AsyncDocumentEndpoint:
    def __init__(self, client: "AsyncIdentisureClient") -> None:
        self._client = client

    async def upload(self, data: bytes, filename: str, mime_type: str = "application/pdf") -> DocumentUploadResponse:
        files = {"file": (filename, data, mime_type)}
        return await self._client._post_multipart("/v3/document", files, _upload_adapter)

    async def download(self, id: str) -> bytes:
        return await self._client._get_bytes(f"/v3/document/{id}")
