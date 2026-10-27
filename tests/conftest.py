from __future__ import annotations

import json
import threading
from collections.abc import Iterator
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pytest

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def fixture_text(name: str) -> str:
    return (FIXTURES / name).read_text()


def fixture(name: str) -> dict[str, Any]:
    data: dict[str, Any] = json.loads(fixture_text(name))
    return data


@dataclass
class Request:
    method: str
    path: str
    headers: dict[str, str]
    body: bytes


class MockServer:
    def __init__(self) -> None:
        self.responses: list[tuple[int, bytes]] = []
        self.requests: list[Request] = []
        self._lock = threading.Lock()
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), self._handler())
        self._thread = threading.Thread(
            target=self._server.serve_forever, args=(0.01,), daemon=True
        )

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self._server.server_port}"

    def enqueue(self, status: int, name: str) -> None:
        self.responses.append((status, fixture_text(name).encode()))

    def calls(self) -> list[tuple[str, str]]:
        return [(r.method, r.path) for r in self.requests]

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()

    def _handler(self) -> type[BaseHTTPRequestHandler]:
        server = self

        class Handler(BaseHTTPRequestHandler):
            def _serve(self) -> None:
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length)
                with server._lock:
                    server.requests.append(
                        Request(self.command, self.path, dict(self.headers), body)
                    )
                    status, payload = server.responses.pop(0)
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            do_GET = _serve
            do_POST = _serve
            do_DELETE = _serve

            def log_message(self, format: str, *args: Any) -> None:
                pass

        return Handler


@pytest.fixture
def server() -> Iterator[MockServer]:
    mock = MockServer()
    mock.start()
    yield mock
    mock.stop()
