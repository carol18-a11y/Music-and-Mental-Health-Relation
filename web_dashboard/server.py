#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys

DEFAULT_PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run_server():
    port = DEFAULT_PORT
    for p in range(DEFAULT_PORT, DEFAULT_PORT + 20):
        try:
            with socketserver.TCPServer(("", p), Handler) as httpd:
                print(f"\n========================================================")
                print(f"🎵 AudioMental UI Dashboard is running!")
                print(f"👉 Local URL: http://localhost:{p}")
                print(f"👉 Serving directory: {DIRECTORY}")
                print(f"========================================================\n")
                print("Press Ctrl+C to stop the server.\n")
                httpd.serve_forever()
                break
        except OSError:
            continue

if __name__ == "__main__":
    run_server()
