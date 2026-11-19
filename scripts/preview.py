#!/usr/bin/env python3
"""Serve the public Studio directory locally with its GitHub Pages URL prefix."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

PUBLIC_DIR = Path(__file__).resolve().parents[1] / "site"
BASE_PATH = "/studio/"


class StudioHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Keep the original request path for correct directory redirects.
        # The standard handler normalizes paths within PUBLIC_DIR.
        if urlsplit(path).path.startswith(BASE_PATH):
            path = path[len(BASE_PATH) - 1 :]
        return super().translate_path(path)

    def _is_studio_request(self):
        path = urlsplit(self.path).path
        if path in ("/", "/studio"):
            self.send_response(302)
            self.send_header("Location", BASE_PATH)
            self.end_headers()
            return False
        if not path.startswith(BASE_PATH):
            self.send_error(404)
            return False
        return True

    def do_GET(self):
        if self._is_studio_request():
            super().do_GET()

    def do_HEAD(self):
        if self._is_studio_request():
            super().do_HEAD()

    def send_error(self, code, message=None, explain=None):
        fallback = PUBLIC_DIR / "404.html"
        if code == 404 and fallback.is_file():
            body = fallback.read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
            return
        super().send_error(code, message, explain)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=4174)
    args = parser.parse_args()
    handler = partial(StudioHandler, directory=str(PUBLIC_DIR))
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    print(f"Studio preview: http://127.0.0.1:{args.port}{BASE_PATH}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
