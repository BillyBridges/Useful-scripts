#FOR WINDOWS
import os
import shutil

#This script counts the number of files of each extension inside the
#informed folder

def search_folder(folder_path, extensions_count, extensions_list):
    """Recursively searches for files in a folder and its subfolders, 
       and calls count_extensions() for each file."""

    fcount = 0
    for root, _, files in os.walk(folder_path):  # os.walk() for recursive traversal
        for filename in files:
            
            count_extensions(filename, extensions_count, extensions_list)  # Call the processing function
            fcount += 1
           
            if fcount % 100 == 0:
                print(fcount, " files checked...")
                
    print(fcount, " files have been checked.")
 

def count_extensions(filepath, extensions_count, extensions_list):
    """Counts file extensions and updates the provided dictionary and list."""

    _, ext = os.path.splitext(filepath)
    ext = ext.lower()  # Case-insensitive
    
    if ext:  # Only process files with extensions
        if ext in extensions_count:
            extensions_count[ext] += 1
        else:
            extensions_count[ext] = 1
            extensions_list.append(ext)  # Add new extension to the list
    else:
        extensions_count["null"] += 1

def display_extension_counts(extensions_count, extensions_list):
    """Displays the counted extensions and their counts."""

    print("\n--- File Extension Summary by Name ---")

    # Sort extensions by count in descending order
    for ext in sorted(extensions_list):  # Sort extensions for consistent output
        count = extensions_count[ext]
        print(f"{ext}: {count}")
        
    sorted_extensions = sorted(extensions_list, key=lambda ext: extensions_count[ext], reverse=True)
    print("\n--- File Extension Summary by Ocurrence ---")
    for ext in sorted_extensions:
        count = extensions_count[ext]
        print(f"{ext}: {count}")

if __name__ == '__main__':
    source_folder = input("Enter the directory to search: ")        
        
    extensions_count = {}
    extensions_list = []
    extensions_count["null"] = 0
    extensions_list.append("null")
    search_folder(source_folder, extensions_count, extensions_list)
    display_extension_counts(extensions_count, extensions_list)