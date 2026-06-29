#!/usr/bin/env python3
"""정적 PWA 개발 서버 — app/ 디렉터리를 PORT(기본 5183)로 서빙.

PORT 환경변수를 읽어 바인딩한다(프리뷰 하니스 호환). 운영 배포는 server/main.py(FastAPI).
"""
import functools
import http.server
import os
import socketserver

ROOT = os.path.join(os.path.dirname(__file__), "..", "app")
PORT = int(os.environ.get("PORT", "5183"))


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      ".json": "application/json", ".svg": "image/svg+xml",
                      ".webmanifest": "application/manifest+json"}

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), functools.partial(Handler, directory=ROOT)) as httpd:
        print(f"무역풍 dev server → http://localhost:{PORT}")
        httpd.serve_forever()
