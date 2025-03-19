#FOR WINDOWS
import os
import shutil
import hashlib
import subprocess

#Recursively deletes files of the informed extensions.
#Example: ".pdf.txt.doc" deletes all .pdf, .txt and .doc files.
#Do not include quotation marks.

def search_folder(folder_path, flext):
    """Recursively searches for files in a folder and its subfolders, 
       and calls iterate_file() for each file."""
    fcount = 0
    pcount = 0
    for root, _, files in os.walk(folder_path):  # os.walk() for recursive traversal
        for filename in files:
            filepath = os.path.join(root, filename)  # Full path to the file
            pcount += iterate_file(filepath, flext)  # Call the processing function
            fcount += 1
           
            if fcount % 100 == 0:
                print(fcount, " files checked...")
                print(pcount, " files processed...")
                
    print(fcount, " files have been checked.")
    print(pcount, " files have been processed.")
    
def iterate_file(filepath, file_extension):
    base, ext = os.path.splitext(filepath)  # Split filename and extension

    if (f"{ext.lower()}." in f"{file_extension.lower()}.") and (ext != ""):  # Case-insensitive extension comparison
        try:
            os.remove(filepath)
            print(f"Deleted: {filepath}")
            return 1
        except Exception as e:
            print(f"Access denied: {e}. Attempting to remove attributes...")
            try:
                subprocess.run(["attrib", "-r", filepath], check=True)
                os.remove(filepath)
                print(f"Deleted: {filepath}")
                return 1
            except Exception as e:
                print(f"Failed to delete file: {filepath}: {e}")
                return 0
    return 0

if __name__ == '__main__':
    source_folder = input("Enter the directory to delete from: ")
    file_ext = input("Enter the file extensions(include dot): ")
    search_folder(source_folder, file_ext)
