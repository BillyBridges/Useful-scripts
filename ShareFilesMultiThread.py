#FOR WINDOWS
import sys
import os
import re
import socket
import threading
import urllib.parse
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

# Shares directory via local network

# Configuration
SERVE_DIRECTORY = sys.argv[1]
PORT = 8000

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class RangeRequestHandler(SimpleHTTPRequestHandler):
    """
    Extends SimpleHTTPRequestHandler to support HTTP Range Requests,
    enabling seeking/scrubbing in video and audio files.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SERVE_DIRECTORY, **kwargs)

    def do_GET(self):
        """Handle GET requests, including Range requests for seeking."""
        if self.headers.get('Range'):
            self.handle_range_request()
        else:
            super().do_GET()

    def handle_range_request(self):
        """Processes the Range header and returns only the requested part of the file."""
        path = self.translate_path(self.path)
        if not os.path.isfile(path):
            self.send_error(404)
            return

        file_size = os.path.getsize(path)
        range_header = self.headers.get('Range')
        
        # Parse the range header (e.g., "bytes=0-499")
        match = re.match(r'bytes=(\d+)-(\d*)', range_header)
        if not match:
            self.send_error(400, "Invalid Range header")
            return

        start = int(match.group(1))
        end = match.group(2)
        end = int(end) if end else file_size - 1

        if start >= file_size:
            self.send_error(416, "Requested Range Not Satisfiable")
            return

        length = end - start + 1
        
        try:
            with open(path, 'rb') as f:
                f.seek(start)
                self.send_response(206) # Partial Content
                self.send_header('Content-type', self.guess_type(path))
                self.send_header('Accept-Ranges', 'bytes')
                self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
                self.send_header('Content-Length', str(length))
                self.end_headers()
                
                # Stream only the requested part
                self.copy_chunked(f, self.wfile, length)
        except Exception as e:
            print(f"Error during range request: {e}")

    def copy_chunked(self, source, dest, length):
        """Helper to copy exactly 'length' bytes from source to destination."""
        buffer_size = 64 * 1024
        while length > 0:
            to_read = min(length, buffer_size)
            buf = source.read(to_read)
            if not buf:
                break
            dest.write(buf)
            length -= len(buf)

    def log_message(self, format, *args):
        # Optional: Suppress standard logs to keep console clean during heavy seeking
        pass

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def run_server():
    server_address = ("", PORT)
    httpd = ThreadedHTTPServer(server_address, RangeRequestHandler)
    ip = get_local_ip()
    print(f"\nSERVER RUNNING: http://{ip}:{PORT}")
    print(f"Seeking enabled. You can now scrub through videos.")
    httpd.serve_forever()

if __name__ == "__main__":
    if not os.path.isdir(SERVE_DIRECTORY):
        print(f"Error: {SERVE_DIRECTORY} not found.")
    else:
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")