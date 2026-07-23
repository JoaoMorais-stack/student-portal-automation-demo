from __future__ import annotations

import json
import mimetypes
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from .automation import PortalClient
from .store import PortalStore


STATIC_DIR = Path(__file__).resolve().parent / "static"
LESSON_ROUTE = re.compile(r"^/api/lessons/([^/]+)/complete$")


class DemoHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, server_address: tuple[str, int], store: PortalStore | None = None) -> None:
        self.store = store or PortalStore()
        super().__init__(server_address, PortalRequestHandler)


class PortalRequestHandler(BaseHTTPRequestHandler):
    server: DemoHTTPServer

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_json(self, payload: dict | list, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_static(self, filename: str) -> None:
        safe_name = Path(filename).name
        path = STATIC_DIR / safe_name
        if not path.is_file():
            self._send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
            return
        body = path.read_bytes()
        content_type, _ = mimetypes.guess_type(path.name)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'; img-src 'self' data:")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/state":
            self._send_json(self.server.store.snapshot())
        elif path == "/api/health":
            self._send_json({"status": "ok", "scope": "local-mock-only"})
        elif path in ("/", "/index.html"):
            self._send_static("index.html")
        elif path.startswith("/static/"):
            self._send_static(path.removeprefix("/static/"))
        else:
            self._send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/reset":
            self._send_json(self.server.store.reset())
            return

        if path == "/api/demo/run":
            host, port = self.server.server_address[:2]
            local_host = "127.0.0.1" if host in ("", "0.0.0.0") else host
            events = PortalClient(f"http://{local_host}:{port}").run()
            self._send_json({"events": [event.to_dict() for event in events], "state": self.server.store.snapshot()})
            return

        match = LESSON_ROUTE.match(path)
        if match:
            lesson_id = unquote(match.group(1))
            lesson, changed = self.server.store.complete_lesson(lesson_id)
            if lesson is None:
                self._send_json({"error": "Lesson not found"}, HTTPStatus.NOT_FOUND)
                return
            self._send_json({"lesson_id": lesson.id, "changed": changed, "completed": lesson.completed})
            return

        self._send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)


def make_server(host: str = "127.0.0.1", port: int = 8765, store: PortalStore | None = None) -> DemoHTTPServer:
    if host not in ("127.0.0.1", "localhost", "::1"):
        raise ValueError("The demo server may bind only to a loopback address.")
    return DemoHTTPServer((host, port), store)

