#!/usr/bin/env python3
"""
Simple Speed Test - local server.

Serves the speed test page and provides three tiny endpoints that the page
uses when you choose "Local network" mode:

    GET  /__down?bytes=N   sends N bytes (used to measure download speed)
    POST /__up             receives and discards data (upload speed)
    GET  /__meta           tells the page this server is running

Why this is useful: run it on a computer connected to your router, then open
the printed "phone / other device" address on a phone or laptop over Wi-Fi.
The result is the speed of your Wi-Fi alone, not your internet plan.

Usage:
    python3 server.py          (port 8080)
    python3 server.py 9000     (choose another port)
    python3 server.py --no-browser   (don't open the browser automatically)

Needs only Python 3.8+ - no extra packages.
"""

import json
import os
import socket
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
CHUNK = os.urandom(64 * 1024)  # random data so nothing along the way can compress it
MAX_DOWNLOAD = 200 * 1024 * 1024  # cap a single request at 200 MB
READ_SIZE = 64 * 1024


class SpeedTestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HERE, **kwargs)

    # Allow the page to be opened from another address and still use this server.
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def log_message(self, fmt, *args):
        # Keep the terminal quiet during tests; only show page loads.
        if "/__" not in self.path:
            super().log_message(fmt, *args)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/__down":
            self._send_download(url)
        elif url.path == "/__meta":
            body = json.dumps({"app": "speedtest-local", "host": socket.gethostname()}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/__up":
            self.send_error(404)
            return
        remaining = int(self.headers.get("Content-Length") or 0)
        try:
            while remaining > 0:
                data = self.rfile.read(min(READ_SIZE, remaining))
                if not data:
                    break
                remaining -= len(data)
        except (ConnectionError, TimeoutError):
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", "2")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b"ok")

    def _send_download(self, url):
        try:
            size = int(parse_qs(url.query).get("bytes", ["0"])[0])
        except ValueError:
            size = 0
        size = max(0, min(size, MAX_DOWNLOAD))
        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Length", str(size))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            while size > 0:
                piece = CHUNK if size >= len(CHUNK) else CHUNK[:size]
                self.wfile.write(piece)
                size -= len(piece)
        except (ConnectionError, TimeoutError):
            pass  # the browser stops downloads when the timed test ends


def lan_ip():
    """Best guess at this computer's address on the local network."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))  # no packet is actually sent
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    port = int(args[0]) if args else 8080
    server = ThreadingHTTPServer(("0.0.0.0", port), SpeedTestHandler)
    server.daemon_threads = True
    ip = lan_ip()
    print("\nSimple Speed Test is running.\n")
    print(f"  On this computer:          http://localhost:{port}")
    if ip:
        print(f"  On a phone / other device: http://{ip}:{port}   (same Wi-Fi)")
    print("\nPress Ctrl+C to stop.\n")
    # Open the test page in this computer's browser once the server is up.
    if "--no-browser" not in sys.argv:
        threading.Timer(1.0, webbrowser.open, [f"http://localhost:{port}"]).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
