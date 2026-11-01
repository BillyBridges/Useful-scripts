import os
import socket
import socketserver 
import threading
import time
import json
import re # Required for robust file name extraction
from http.server import SimpleHTTPRequestHandler, HTTPServer
from typing import Dict

# Import the new multipart parsing logic
from multipart_parser_logic import stream_multipart_upload, extract_boundary

# --- Configuration ---
# IMPORTANT: Define the root directory for both serving (downloads) and saving (uploads).
# Ensure this path exists and is easily accessible.
SERVE_DIRECTORY = r'D:\OpenNet' 

PORT = 8000
# ---------------------

# --- HTML Client (Embedded) ---
TRANSFER_CLIENT_HTML = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>One-Way Local Upload</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #f0f4f8;
            color: #1f2937;
            min-height: 10vh;
        }}
        .container {{
            max-width: 600px;
        }}
        .upload-area-buttons {{
            border: 3px solid #3b82f6;
            background-color: #e0f2fe;
            transition: all 0.3s ease;
        }}
        .file-list-item {{
            animation: fadeIn 0.3s ease-out;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(5px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .btn {{
            transition: background-color 0.3s, transform 0.1s;
        }}
        .btn:active {{
            transform: scale(0.98);
        }}
    </style>
</head>
<body class="flex flex-col items-center justify-center p-4">

    <div class="container w-full bg-white p-6 md:p-8 rounded-xl shadow-2xl border border-blue-200">
        <h1 class="text-3xl font-extrabold mb-2 text-center text-blue-700">
            Local Upload Hub
        </h1>
        <p class="text-sm text-center text-gray-500 mb-6">
            Upload files from your device to this PC (Target Folder: <code>{SERVE_DIRECTORY}</code>)
        </p>
        
        <!-- Progress Bar -->
        <div id="progressBarContainer" class="hidden mb-4">
            <div class="flex justify-between mb-1">
                <span class="text-xs font-medium text-blue-700">Upload Progress:</span>
                <span id="progressText" class="text-xs font-medium text-blue-700">0%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2.5">
                <div id="progressBar" class="bg-blue-600 h-2.5 rounded-full transition-all duration-100 ease-linear" style="width: 0%"></div>
            </div>
        </div>

        <!-- Status Message Box -->
        <div id="statusMessage" class="hidden mb-4 p-3 rounded-lg text-sm font-medium border" role="alert"></div>

        <form id="uploadForm" class="space-y-4">
            
            <!-- File Selection Inputs (Hidden) -->
            <input type="file" id="fileOnlyInput" name="file" multiple class="hidden" 
                    onchange="handleFileSelection(this.files, 'file')">
            <input type="file" id="folderInput" name="folder" multiple class="hidden" 
                    webkitdirectory directory 
                    onchange="handleFileSelection(this.files, 'folder')">

            <!-- Buttons to trigger the inputs -->
            <div class="upload-area-buttons p-4 rounded-lg">
                <p class="text-center text-md text-blue-800 font-semibold mb-3">
                    Select Upload Type
                </p>
                <div class="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-3">
                    <button type="button" onclick="document.getElementById('fileOnlyInput').click()" 
                        class="flex-1 py-3 px-4 bg-green-600 text-white font-semibold rounded-lg shadow-md hover:bg-green-700 btn flex items-center justify-center">
                        <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-3-3v6m-6 3h12a2 2 0 002-2V7a2 2 0 00-2-2H9a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
                        Files Only
                    </button>
                    <button type="button" onclick="document.getElementById('folderInput').click()" 
                        class="flex-1 py-3 px-4 bg-yellow-600 text-white font-semibold rounded-lg shadow-md hover:bg-yellow-700 btn flex items-center justify-center">
                        <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" /></svg>
                        Entire Folder
                    </button>
                </div>
            </div>

            <!-- File List -->
            <div id="fileList" class="space-y-2 max-h-48 overflow-y-auto p-3 border border-gray-300 rounded-lg bg-gray-50">
                <p class="text-center text-gray-400 text-sm italic">No files selected.</p>
            </div>

            <button type="submit" id="submitButton" 
                class="btn w-full py-3 px-4 bg-blue-600 text-white font-semibold rounded-lg shadow-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                disabled>
                Upload Selected Files
            </button>
        </form>
    </div>

    <script>
        const uploadUrl = window.location.origin + window.location.pathname;
        
        const fileOnlyInput = document.getElementById('fileOnlyInput');
        const folderInput = document.getElementById('folderInput');
        const fileListDiv = document.getElementById('fileList');
        const submitButton = document.getElementById('submitButton');
        const uploadForm = document.getElementById('uploadForm');
        const statusMessage = document.getElementById('statusMessage');

        // New DOM references for progress bar
        const progressBarContainer = document.getElementById('progressBarContainer');
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');

        // Global variable to store the currently selected files (from either input)
        let selectedFiles = [];

        function formatBytes(bytes, decimals = 2) {{
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const dm = decimals < 0 ? 0 : decimals;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
        }}

        function displayStatus(message, type = 'info') {{
            statusMessage.textContent = message;
            statusMessage.classList.remove('hidden', 'bg-red-100', 'text-red-800', 'bg-green-100', 'text-green-800', 'bg-yellow-100', 'text-yellow-800', 'border-red-400', 'border-green-400', 'border-yellow-400');
            
            if (type === 'success') {{
                statusMessage.classList.add('bg-green-100', 'text-green-800', 'border-green-400');
            }} else if (type === 'error') {{
                statusMessage.classList.add('bg-red-100', 'text-red-800', 'border-red-400');
            }} else {{
                statusMessage.classList.add('bg-yellow-100', 'text-yellow-800', 'border-yellow-400');
            }}
            statusMessage.classList.remove('hidden');
        }}

        function resetProgressUI() {{
            progressBarContainer.classList.add('hidden');
            progressBar.style.width = '0%';
            progressText.textContent = '0%';
        }}

        function updateFileListUI() {{
            fileListDiv.innerHTML = '';
            
            if (selectedFiles.length === 0) {{
                fileListDiv.innerHTML = '<p class="text-center text-gray-400 text-sm italic p-2">No files selected.</p>';
                submitButton.disabled = true;
                return;
            }}
            
            let totalSize = 0;
            const fragment = document.createDocumentFragment();

            for (const file of selectedFiles) {{
                totalSize += file.size;
                const listItem = document.createElement('div');
                listItem.className = 'file-list-item flex justify-between items-center text-gray-700 text-sm p-1.5 bg-white rounded-md border border-gray-200';
                
                // Use webkitRelativePath for folder structure display
                const path = file.webkitRelativePath || file.name;
                
                listItem.innerHTML = `
                    <span class="truncate pr-2" title="${{path}}">${{path}}</span>
                    <span class="text-xs text-gray-500 ml-2 whitespace-nowrap">${{formatBytes(file.size)}}</span>
                `;
                fragment.appendChild(listItem);
            }}
            
            const totalSummary = document.createElement('p');
            totalSummary.className = 'mt-2 text-xs font-semibold text-gray-600 pt-2 border-t border-gray-200';
            totalSummary.textContent = `Total items: ${{selectedFiles.length}} | Total size: ${{formatBytes(totalSize)}}`;
            fragment.appendChild(totalSummary);

            fileListDiv.appendChild(fragment);
            submitButton.disabled = false;
            displayStatus(`Ready to upload ${{selectedFiles.length}} item(s).`, 'info');
        }}

        function handleFileSelection(files, type) {{
            // Ensure any files previously selected by the *other* input are cleared from the UI
            selectedFiles = Array.from(files);
            
            // Clear the other input's value to prevent unexpected behavior
            if (type === 'file' && folderInput.value) {{
                folderInput.value = '';
            }} else if (type === 'folder' && fileOnlyInput.value) {{
                fileOnlyInput.value = '';
            }}
            
            updateFileListUI();
        }}


        uploadForm.addEventListener('submit', (e) => {{
            e.preventDefault();
            
            if (selectedFiles.length === 0) {{
                displayStatus('Please select at least one file or folder.', 'error');
                return;
            }}

            // 1. Setup UI for Upload
            resetProgressUI();
            progressBarContainer.classList.remove('hidden');
            submitButton.disabled = true;
            submitButton.textContent = 'Uploading... (0%)';
            displayStatus('Initiating upload (may take time for folders/large files)...', 'info');

            const formData = new FormData();
            for (const file of selectedFiles) {{
                // Use the relative path as the field name to send path metadata to the server
                const path = file.webkitRelativePath || file.name;
                // CRITICAL: The third argument (filename) sends the relative path to the server
                formData.append('file', file, path); 
            }}
            
            // 2. Use XMLHttpRequest for reliable progress tracking
            const xhr = new XMLHttpRequest();
            
            // Progress Handler
            xhr.upload.onprogress = function(event) {{
                if (event.lengthComputable) {{
                    const percent = Math.round((event.loaded / event.total) * 100);
                    progressBar.style.width = percent + '%';
                    progressText.textContent = percent + '%';
                    submitButton.textContent = `Uploading... (${{percent}}%)`;
                }}
            }};
            
            // Completion/Success Handler
            xhr.onload = function() {{
                resetProgressUI();
                if (xhr.status === 200) {{
                    try {{
                        const result = JSON.parse(xhr.responseText);
                        displayStatus(result.message || 'Upload complete!', 'success');
                    }} catch (e) {{
                        displayStatus('Upload succeeded, but server response was invalid.', 'error');
                    }}
                    
                    // Clear inputs and file list
                    fileOnlyInput.value = '';
                    folderInput.value = '';
                    selectedFiles = [];
                    updateFileListUI();
                }} else {{
                    // Server returned an error status (4xx, 5xx)
                    let errorMsg = `Server status ${{xhr.status}}`;
                    try {{
                        const result = JSON.parse(xhr.responseText);
                        errorMsg += `: ${{result.message}}`;
                    }} catch (e) {{
                        // Fallback to raw text if JSON parsing fails
                        errorMsg += `. Details: ${{xhr.responseText.substring(0, 100)}}...`;
                    }}
                    displayStatus(`Upload failed: ${{errorMsg}}`, 'error');
                }}
                submitButton.disabled = false;
                submitButton.textContent = 'Upload Selected Files';
            }};
            
            // Error Handler (Network errors, timeouts)
            xhr.onerror = function() {{
                resetProgressUI();
                displayStatus(`Network Error: Could not connect to PC at ${{window.location.host}}. Check connection and firewall.`, 'error');
                submitButton.disabled = false;
                submitButton.textContent = 'Upload Selected Files';
            }};

            // 3. Send Request
            xhr.open('POST', uploadUrl);
            xhr.send(formData);
        }});

        // Initial setup
        updateFileListUI();
    </script>
</body>
</html>
"""

def get_local_ip():
    """Tries to find the local network IP address of the machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1)) # Use a non-routable address to force local binding
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1' 
    finally:
        s.close()
    return IP

class TwoWayTransferHandler(SimpleHTTPRequestHandler):
    """
    Handles only GET (serving HTML client) and POST (uploads) requests.
    Uses stream_multipart_upload from multipart_parser_logic for POST handling.
    """
    
    def __init__(self, *args, **kwargs):
        # We pass the SERVE_DIRECTORY to satisfy SimpleHTTPRequestHandler base class,
        # but we no longer use its directory browsing features for security.
        super().__init__(*args, directory=SERVE_DIRECTORY, **kwargs)

    def _send_json_response(self, status_code: int, status: str, message: str):
        """Helper to send JSON response with specified status code."""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_data = {"status": status, "message": message}
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def do_GET(self):
        """
        Serves the HTML client on the root path, otherwise returns 404 (no download access).
        """
        if self.path == '/' or self.path == '/index.html':
            content = TRANSFER_CLIENT_HTML.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-length', len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            # Explicitly deny access to other paths (no file browsing/download)
            self._send_json_response(404, "error", "PC download access has been disabled.")

    def do_POST(self):
        """Handle file uploads via POST."""
        if self.path != '/':
            return self.get_error_response(404, "Invalid upload path.")
        
        post_length = self.headers.get('Content-Length')
        content_type = self.headers.get('Content-Type') # Use .get() for safety
        
        if not post_length or not content_type:
            return self.get_error_response(400, "Missing Content-Length or Content-Type header.")

        try:
            post_length = int(post_length)
        except ValueError:
            return self.get_error_response(400, "Invalid Content-Length header.")

        # --- FIX: Ensure Content-Type is a string before passing to the parser ---
        # self.headers.get('Content-Type') should already return a string, 
        # but explicitly handle if it somehow returned an object (e.g., in Python 2 or older/different http implementation).
        # The standard Python 3 http.server/http.client headers collection
        # provides item access or .get() which returns the string value of the header.
        # We ensure it is cast to string and not the entire HTTPMessage object.
        content_type_string = str(content_type)
        
        # Call the streaming parser
        try:
            print(f"[Parser] Target directory: {SERVE_DIRECTORY}")
            file_count, message = stream_multipart_upload(
                self.rfile, 
                content_type_string, # Pass the guaranteed string value
                SERVE_DIRECTORY, 
                post_length
            )
            
            # Success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message': message, 'file_count': file_count}).encode('utf-8'))
            
        except ValueError as e:
            # Errors raised by the parser (e.g., boundary not found, invalid filename)
            print(f"[Parser] Critical Error: {e}")
            self.get_error_response(400, f"Upload Error: {e}")
        except Exception as e:
            # General operational errors (e.g., IOError, disk full)
            print(f"[Server] Unhandled exception during upload: {e}")
            self.get_error_response(500, f"Server Error during upload: {e}")
            
    # The original handle_upload method is removed, replaced by the call to stream_multipart_upload

    def log_message(self, format, *args):
        # Suppress routine console logging
        pass

class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer): 
    pass

def run_server():
    """Starts the HTTP server on a separate thread."""
    
    # 1. Check/Create Directory
    if not os.path.isdir(SERVE_DIRECTORY):
        try:
            os.makedirs(SERVE_DIRECTORY)
            print(f"Created directory: '{SERVE_DIRECTORY}'")
        except Exception as e:
            print(f"Error: Could not create directory '{SERVE_DIRECTORY}'. {e}")
            return

    # 2. Start the Server
    global httpd
    server_address = ("", PORT)
    httpd = ThreadingHTTPServer(server_address, TwoWayTransferHandler)
    
    local_ip = get_local_ip()
    print("-" * 50)
    print("--- PC One-Way Local Upload Hub (Streaming) ---")
    print(f"Target Folder: {os.path.abspath(SERVE_DIRECTORY)}")
    print(f"Access URL: http://{local_ip}:{PORT}/")
    print("--------------------------------------------------")
    print("IMPORTANT: Connect your mobile device to the same WiFi.")
    print("--------------------------------------------------")
    
    # Serve the server indefinitely until Ctrl+C
    httpd.serve_forever()

if __name__ == "__main__":
    try:
        server_thread = threading.Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()

        print("\nPress Ctrl+C to stop the server and exit.")
        
        while server_thread.is_alive():
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down server...")
        if 'httpd' in globals():
            httpd.shutdown()
        print("Server stopped.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")