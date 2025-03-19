#FOR WINDOWS
import os
import hashlib

#This script deletes files of equal content contained anywhere inside 
#the informed directory or its subfolders. It has the down side that
#it stores a list of file paths in memory so it can be too memory
#consuming. It also doesn't deal with permissions for when the files
#are read-only and cannot be deleted, so it isn't very robust. 

"""
def calculate_file_hash(file_path):
    #Calculates the hash value of a file's content.
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hasher.update(chunk)
    file_size = os.path.getsize(file_path)
    file_size_hex = f"{file_size}"
    return hasher.hexdigest() + file_size_hex
"""

def calculate_file_hash(file_path):
    #Calculates the hash value of a file's content (SHA-256) and returns it with file size as a hexadecimal string.
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hasher.update(chunk)

    file_size = os.path.getsize(file_path)
    file_size_hex = f"{file_size}"

    combined_value = hasher.hexdigest() + file_size_hex
    return combined_value

def find_duplicate_files(root_folder):
    #Traverses through the root folder and identifies duplicate files.
    fcount = 0
    duplicates = {}
    for folder_path, _, file_names in os.walk(root_folder):
        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)
            file_hash = calculate_file_hash(file_path)
            #print(file_hash)
            if file_hash in duplicates:
                duplicates[file_hash].append(file_path)
            else:
                duplicates[file_hash] = [file_path]
            fcount += 1
            if fcount % 400 == 0:
                print(fcount, " files checked...")
    print(fcount, " files have been checked.")
    return duplicates

def remove_duplicate_files(duplicates):
    #Removes duplicate files from the file system.
    delcount = 0
    for file_paths in duplicates.values():
        if len(file_paths) > 1:
            #print(f"Duplicate files found:\n{file_paths}\n")
            for file_path in file_paths[1:]:
                os.remove(file_path)
                delcount += 1
                if delcount % 500 == 0:
                    print(delcount, " files deleted...")
                #print(f"{file_path} has been deleted.\n")
    print(delcount, " files have been deleted.")

if __name__ == '__main__':
    root_folder = input("Enter the directory to check for duplicates: ")
    duplicates = find_duplicate_files(root_folder)
    remove_duplicate_files(duplicates)
  
