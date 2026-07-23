from __future__ import annotations

import ipaddress
import json
from dataclasses import dataclass, asdict
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen


class AutomationSafetyError(ValueError):
    """Raised when a target is outside the authorized local mock environment."""


class PortalConnectionError(RuntimeError):
    """Raised when the local demo portal cannot be reached."""


def validate_local_base_url(base_url: str) -> str:
    parsed = urlparse(base_url)
    if parsed.scheme != "http":
        raise AutomationSafetyError("Only plain HTTP is accepted for this local demo.")
    if not parsed.hostname or parsed.username or parsed.password:
        raise AutomationSafetyError("The demo URL must contain only a local host and port.")

    hostname = parsed.hostname.lower()
    is_localhost = hostname == "localhost"
    try:
        is_loopback = ipaddress.ip_address(hostname).is_loopback
    except ValueError:
        is_loopback = False

    if not (is_localhost or is_loopback):
        raise AutomationSafetyError("Automation is restricted to loopback addresses.")
    if parsed.path not in ("", "/") or parsed.query or parsed.fragment:
        raise AutomationSafetyError("Use only the local portal origin, without a path or query.")
    return base_url.rstrip("/")


@dataclass(frozen=True)
class AutomationEvent:
    lesson_id: str
    lesson_title: str
    course_title: str
    result: str

    def to_dict(self) -> dict:
        return asdict(self)


class PortalClient:
    def __init__(self, base_url: str, timeout: float = 3.0) -> None:
        self.base_url = validate_local_base_url(base_url)
        self.timeout = timeout

    def _json_request(self, method: str, path: str) -> dict:
        request = Request(
            f"{self.base_url}{path}",
            data=b"{}" if method == "POST" else None,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            method=method,
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError) as exc:
            raise PortalConnectionError(f"Local portal request failed: {exc}") from exc

    def state(self) -> dict:
        return self._json_request("GET", "/api/state")

    def complete_lesson(self, lesson_id: str) -> dict:
        safe_id = quote(lesson_id, safe="")
        return self._json_request("POST", f"/api/lessons/{safe_id}/complete")

    def run(self, on_event: Callable[[AutomationEvent], None] | None = None) -> list[AutomationEvent]:
        events: list[AutomationEvent] = []
        for course in self.state()["courses"]:
            for lesson in course["lessons"]:
                if lesson["completed"]:
                    continue
                response = self.complete_lesson(lesson["id"])
                event = AutomationEvent(
                    lesson_id=lesson["id"],
                    lesson_title=lesson["title"],
                    course_title=course["title"],
                    result="completed" if response["changed"] else "already-completed",
                )
                events.append(event)
                if on_event:
                    on_event(event)
        return events

