"""Offline-safe HTTP endpoint sketch for BIL preference events.

This stdlib server is intentionally simple and optional. It demonstrates the
endpoint shape without activating live NAS wiring or requiring external packages.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from .bil_api import build_preference_event
from .bil_models import PreferenceCounter
from .config import DEFAULT_BIND_HOST, DEFAULT_PORT

MODEL = PreferenceCounter()

class BILHandler(BaseHTTPRequestHandler):
    """Handle minimal preference-event ingestion requests."""

    def do_POST(self) -> None:
        if self.path not in {"/bil/event", "/preference-event"}:
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("content-length", "0") or 0)
            payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
            event = build_preference_event(
                signal=payload.get("signal", "accidental_visit"),
                source=payload.get("source", "manual_signal"),
                subject=payload.get("subject", ""),
                metadata=payload.get("metadata") or {},
            )
            MODEL.learn_one(event)
            body = json.dumps({"ok": True, "event": event}).encode("utf-8")
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except (json.JSONDecodeError, ValueError) as exc:
            self.send_error(400, str(exc))
        except Exception as exc:
            self.send_error(500, str(exc))

def run(host: str = DEFAULT_BIND_HOST, port: int = DEFAULT_PORT) -> None:
    HTTPServer((host, port), BILHandler).serve_forever()

if __name__ == "__main__":
    run()
