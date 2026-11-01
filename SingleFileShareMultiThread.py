#FOR WINDOWS
import sys
import os
import re
import socket
import threading
import time
import urllib.parse
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

# Shares single file via local network

# --- Configuration ---
# Set this to the EXACT file you want to share
FILE_TO_SHARE = sys.argv[1]
PORT = 8000
# ---------------------

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Allows multiple users to stream/seek the same file simultaneously."""
    daemon_threads = True

class DirectRangeHandler(SimpleHTTPRequestHandler):
    """
    Serves ONE specific file with support for Range Requests (Seeking).
    Does not use 'super()' to avoid falling back to directory listings.
    """
    def do_GET(self):
        if not os.path.isfile(FILE_TO_SHARE):
            self.send_error(404, "File to share not found on disk.")
            return

        # If the browser asks for a specific chunk (Seeking)
        if self.headers.get('Range'):
            self.handle_range_request()
        else:
            # Otherwise, serve the file from the beginning (Normal Playback)
            self.serve_full_file()

    def serve_full_file(self):
        """Standard file serving without seeking."""
        file_size = os.path.getsize(FILE_TO_SHARE)
        filename = os.path.basename(FILE_TO_SHARE)
        # URL encode filename for header safety
        safe_filename = urllib.parse.quote(filename)
        
        try:
            with open(FILE_TO_SHARE, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', self.guess_type(FILE_TO_SHARE))
                self.send_header('Content-Length', str(file_size))
                self.send_header('Accept-Ranges', 'bytes')
                # Dictates the filename shown to the client
                self.send_header('Content-Disposition', f'inline; filename="{safe_filename}"')
                self.end_headers()
                self.copyfile(f, self.wfile)
        except Exception as e:
            print(f"Error serving full file: {e}")

    def handle_range_request(self):
        """Processes the Range header for seeking."""
        file_size = os.path.getsize(FILE_TO_SHARE)
        filename = os.path.basename(FILE_TO_SHARE)
        safe_filename = urllib.parse.quote(filename)
        range_header = self.headers.get('Range')
        
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
            with open(FILE_TO_SHARE, 'rb') as f:
                f.seek(start)
                self.send_response(206) # Partial Content
                self.send_header('Content-type', self.guess_type(FILE_TO_SHARE))
                self.send_header('Accept-Ranges', 'bytes')
                self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
                self.send_header('Content-Length', str(length))
                # Dictates the filename shown to the client
                self.send_header('Content-Disposition', f'inline; filename="{safe_filename}"')
                self.end_headers()
                
                # Stream only the requested part using a chunked copy
                self.copy_chunked(f, self.wfile, length)
        except Exception as e:
            print(f"Error during range request: {e}")

    def copy_chunked(self, source, dest, length):
        """Helper to copy exactly 'length' bytes."""
        buffer_size = 64 * 1024
        while length > 0:
            to_read = min(length, buffer_size)
            buf = source.read(to_read)
            if not buf:
                break
            dest.write(buf)
            length -= len(buf)

    def log_message(self, format, *args):
        # Keeps the console clean
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
    httpd = ThreadedHTTPServer(server_address, DirectRangeHandler)
    ip = get_local_ip()
    print(f"\nDIRECT SEEKING SERVER: http://{ip}:{PORT}")
    print(f"Sharing: {os.path.basename(FILE_TO_SHARE)}")
    httpd.serve_forever()

if __name__ == "__main__":
    if not os.path.isfile(FILE_TO_SHARE):
        print(f"Error: {FILE_TO_SHARE} is not a file.")
    else:
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")