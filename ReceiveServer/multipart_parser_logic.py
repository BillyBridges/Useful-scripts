import os
import re
import json
#import binascii #For debug only
from typing import Dict, BinaryIO, Tuple

# Size of the buffer read from the stream (64KB)
CHUNK_SIZE = 65536 

def extract_boundary(content_type_header: str) -> str:
    """Extracts the boundary string from the Content-Type header."""
    pdict = {}
    parts = content_type_header.split(';')
    for part in parts:
        if '=' in part:
            key, value = part.strip().split('=', 1)
            pdict[key.lower()] = value.strip('\"')

    boundary = pdict.get('boundary')
    if not boundary:
        raise ValueError("Boundary not found in Content-Type header.")
    return boundary

def get_filename_from_headers(content_disposition: str) -> str:
    """Extracts the filename/relative path from the Content-Disposition header."""
    # Use regex to robustly find the filename value
    filename_match = re.search(r'filename=\"([^\"]+)\"', content_disposition)
    if not filename_match:
        raise ValueError("Could not extract filename from Content-Disposition.")
    
    # The value should be the relative path (e.g., 'folder/file.txt' or just 'file.txt')
    relative_path = filename_match.group(1)
    
    # Sanitize the path: remove leading separators and prevent directory traversal
    sanitized_path = relative_path.lstrip(os.path.sep).lstrip('/')
    
    # Simple check against directory traversal attempts
    if '..' in sanitized_path:
        raise ValueError("Directory traversal attempt detected in filename.")
        
    return sanitized_path



def stream_multipart_upload(stream: BinaryIO, content_type: str, target_dir: str, total_post_length: int = None) -> Tuple[int, str]:
    try:
        boundary_str = extract_boundary(content_type)
        boundary_bytes = boundary_str.encode('ascii')
        boundary_prefix = b'\r\n--' + boundary_bytes
        initial_boundary_marker = b'--' + boundary_bytes
    except ValueError as e:
        return 0, str(e)

    # TRACKING BYTES
    bytes_remaining = total_post_length if total_post_length is not None else float('inf')
    
    def safe_read(size):
        nonlocal bytes_remaining
        if bytes_remaining <= 0:
            return b''
        read_size = min(size, bytes_remaining)
        data = stream.read(read_size)
        bytes_remaining -= len(data)
        return data

    file_count = 0
    # Initial read
    read_buffer = safe_read(CHUNK_SIZE)
    
    # 1. Consume Initial Boundary
    idx = read_buffer.find(initial_boundary_marker)
    if idx == -1: return 0, "Initial boundary not found"
    line_end = read_buffer.find(b'\r\n', idx)
    read_buffer = read_buffer[line_end + 2:]

    while True:
        # Check if we are at the end
        if read_buffer.startswith(b'--'): 
            break
        
        # 2a. Headers
        while b'\r\n\r\n' not in read_buffer:
            chunk = safe_read(CHUNK_SIZE)
            if not chunk: break
            read_buffer += chunk
        
        header_end = read_buffer.find(b'\r\n\r\n')
        if header_end == -1: break
        
        header_block = read_buffer[:header_end].decode('latin-1')
        read_buffer = read_buffer[header_end + 4:]
        
        filename = None
        for line in header_block.split('\r\n'):
            if 'filename=' in line.lower():
                filename = get_filename_from_headers(line)

        if filename:
            file_count += 1
            full_path = os.path.join(target_dir, filename)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            print(f"[Parser] Receiving: {filename}")
            
            with open(full_path, 'wb') as f:
                while True:
                    # Look for the boundary
                    b_idx = read_buffer.find(boundary_prefix)
                    # Also check for terminal boundary specifically
                    t_idx = read_buffer.find(b'\r\n--' + boundary_bytes + b'--')
                    
                    stop_idx = -1
                    if b_idx != -1: stop_idx = b_idx
                    if t_idx != -1 and (stop_idx == -1 or t_idx < stop_idx):
                        stop_idx = t_idx

                    if stop_idx != -1:
                        f.write(read_buffer[:stop_idx])
                        read_buffer = read_buffer[stop_idx:]
                        break

                    # Write safely (keeping enough for boundary detection)
                    if len(read_buffer) > (len(boundary_prefix) + 4):
                        keep = len(boundary_prefix) + 4
                        write_size = len(read_buffer) - keep
                        f.write(read_buffer[:write_size])
                        read_buffer = read_buffer[write_size:]
                    
                    chunk = safe_read(CHUNK_SIZE)
                    if not chunk:
                        f.write(read_buffer)
                        read_buffer = b''
                        break
                    read_buffer += chunk

            # Cleanup after file
            if read_buffer.startswith(b'\r\n'):
                read_buffer = read_buffer[2:]
            
            if read_buffer.startswith(initial_boundary_marker):
                read_buffer = read_buffer[len(initial_boundary_marker):]
                if read_buffer.startswith(b'--'): # End of all data
                    break
                if read_buffer.startswith(b'\r\n'):
                    read_buffer = read_buffer[2:]
        else:
            # Skip non-file parts
            while boundary_prefix not in read_buffer and b'--' + boundary_bytes + b'--' not in read_buffer:
                chunk = safe_read(CHUNK_SIZE)
                if not chunk: break
                read_buffer += chunk
            
            skip_idx = read_buffer.find(boundary_prefix)
            if skip_idx == -1: break
            read_buffer = read_buffer[skip_idx + len(boundary_prefix):]
            if read_buffer.startswith(b'\r\n'): read_buffer = read_buffer[2:]

    return file_count, f"{file_count} item(s) uploaded successfully."