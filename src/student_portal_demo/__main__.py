from __future__ import annotations

import argparse
import threading
import webbrowser

from .automation import AutomationSafetyError, PortalClient, PortalConnectionError
from .server import make_server


DEFAULT_URL = "http://127.0.0.1:8765"


def serve(port: int, open_browser: bool) -> int:
    server = make_server(port=port)
    url = f"http://127.0.0.1:{server.server_port}"
    print(f"Student Portal Automation Demo running at {url}")
    print("Press Ctrl+C to stop.")
    if open_browser:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDemo stopped.")
    finally:
        server.server_close()
    return 0


def automate(url: str) -> int:
    try:
        events = PortalClient(url).run()
    except (AutomationSafetyError, PortalConnectionError) as exc:
        print(f"Automation blocked: {exc}")
        return 1
    if not events:
        print("No pending mock lessons were found.")
        return 0
    for event in events:
        print(f"[{event.result}] {event.course_title} / {event.lesson_title}")
    print(f"Completed {len(events)} mock lesson(s).")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local-only student portal automation demo")
    subparsers = parser.add_subparsers(dest="command")

    serve_parser = subparsers.add_parser("serve", help="Start the fictional local portal")
    serve_parser.add_argument("--port", type=int, default=8765)
    serve_parser.add_argument("--no-browser", action="store_true")

    automate_parser = subparsers.add_parser("automate", help="Run authorized automation against the local mock")
    automate_parser.add_argument("--url", default=DEFAULT_URL)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command in (None, "serve"):
        return serve(getattr(args, "port", 8765), not getattr(args, "no_browser", False))
    if args.command == "automate":
        return automate(args.url)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

