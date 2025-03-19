#FOR WINDOWS
import os
import shutil
import hashlib
import subprocess


#This code serves the purpose of searching a folder for files of
#a certain extension informed by the user and moving the file to
#a destination folder, if the destination folder doesn't contain
#a file with the same contents already. If the file already exists
#in the destination folder, the file gets deleted instead. The
#content of the files are compared, not the filename, and for that,
#it will create a hash list inside the destination folder "hash.hsh". 
#It will only verify files it has copied. It'll ignore pre-existing 
#files in the destination folder that are not in the hash list.
#Files with the same name will be renamed.

#This version of the script will actually create a folder inside the
#destination folder and move all the files with the same name before
#the dot, i.e. with the same name disregarding the extension(asso-
#ciated files). But it still hashes only the file that has the extension 
#informed at the beginning. It will also delete associated files in 
#case the main file hashes duplicate.

#IMFORM ONLY ONE EXTENSION


def calculate_file_hash(file_path):
    #Calculates the hash value of a file's content (SHA-256) and returns it with file size as a hexadecimal string.
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                hasher.update(chunk)
    except Exception as e:
        print(f"Failed to hash file: {file_path}: {e}")
        return None

    file_size = os.path.getsize(file_path)
    file_size_hex = f"{file_size}"

    combined_value = hasher.hexdigest() + file_size_hex
    return combined_value
    
def load_hashes_from_file(folder_path):
    """Loads hashes from the file into a set in memory."""
    hash_file_path = os.path.join(folder_path, "hash.hsh")
    hashes = set()
    try:
        with open(hash_file_path, "r") as f:
            for line in f:
                hashes.add(line.strip())
    except FileNotFoundError:
        print("Hash file not found. Attempting to create it...")
        return hashes  # File might not exist yet, handle it later
    except Exception as e:
        print(f"Error reading hash file: {e}")
        raise Exception("Fatal error while attempting to read hash file.")
    return hashes
    
def create_hash_file_handle(folder_path):
    """Creates (or opens for writing) the hash.hsh file and returns a file handle."""
    hash_file_path = os.path.join(folder_path, "hash.hsh")
    try:
        f = open(hash_file_path, "a")  # "a" mode creates/appends
        return f
        
    except Exception as e:
        print(f"Error creating hash file: {e}")
        return None  # Or raise the exception if you prefer
        
def del_ass_file(filepath, pcname, dstfolder, counters):
    base, ext = os.path.splitext(filepath)
    base = os.path.basename(base)
    if (base.lower() != pcname.lower()):
        return 0
        
    try:
        os.remove(filepath)
        print(f"Deleted (duplicate): {filepath}")
        counters["delcount"] += 1
        return 1
    except Exception as e:
        print(f"Access denied: {e}. Attempting to remove attributes...")
        try:            
            subprocess.run(["attrib", "-r", filepath], check=True)          
            os.remove(filepath)
            print(f"Deleted: {filepath}")
            counters["delcount"] += 1
            return 1
        except Exception as e:
            print(f"Failed to delete file: {filepath}: {e}")
            counters["faileddelcount"] += 1
            return 0
            
def move_ass_file(filepath, pcname, dstfolder, counters):
    base, ext = os.path.splitext(filepath)
    base = os.path.basename(base)
    if (base.lower() != pcname.lower()):
        return 0
        
    try:
        filename = os.path.basename(filepath)       
        destination_path = os.path.join(dstfolder, filename)   
        print("Attempting to move file...")
        shutil.move(filepath, destination_path)  # Now move the file
        print(f"Moved: {filepath}")
        counters["movecount"] += 1
        return 1

    except Exception as e:
        print(f"Error moving {filepath}: {e}")
        counters["failedmovecount"] += 1
        return 0 
   
   
def search_folder_flat(folder_path, pcname, dstfolder, counters, func):
    """Searches only the specified folder (no subfolders) and processes files."""

    try:
        for filename in os.listdir(folder_path):  # Use os.listdir()
            filepath = os.path.join(folder_path, filename)

            if os.path.isfile(filepath):  # Check if it's a file (not a directory)
                func(filepath, pcname, dstfolder, counters)
                

    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
          # Or handle the error as you see fit
        raise Exception("failed to search folder for associated files.")
    except NotADirectoryError:
        print(f"Error: '{folder_path}' is not a directory.")
        raise Exception("failed to search folder for associated files.")
    except Exception as e: # Catch other potential exceptions
        print(f"An unexpected error occurred: {e}")
        raise Exception("failed to search folder for associated files.")
    

 

   
def search_folder(folder_path, hshf, dstfolder, flext, hshm, func):
    """Recursively searches for files in a folder and its subfolders, 
       and calls func() for each file."""
    counters = {  # Initialize all counters to 0
        "movecount": 0,
        "delcount": 0,
        "skipcount": 0,
        "failedmovecount": 0,
        "faileddelcount": 0,
        "hashfailcount": 0,
        "extrfailcount": 0,
        "hashsuccessescount": 0,
    }
    fcount = 0
    pcount = 0
    for root, _, files in os.walk(folder_path):  # os.walk() for recursive traversal
        for filename in files:
            filepath = os.path.join(root, filename)  # Full path to the file
            pcount += func(filepath, dstfolder, hshf, flext, hshm, counters)  # Call the processing function
            fcount += 1
           
            if fcount % 100 == 0:
                print(fcount, " files checked...")
                print(pcount, " files processed...")
                
    print(fcount, " files have been checked.")
    print(pcount, " files have been processed.")
    print(counters["movecount"], " Move successes.")
    print(counters["delcount"], " Deletion successes.")
    print(counters["hashsuccessescount"], " Hashing successes.")
    print(counters["skipcount"], " Skips.")
    print(counters["failedmovecount"], " Move fails.")
    print(counters["faileddelcount"], " Deletion fails.")
    print(counters["hashfailcount"], " Hash fails.")
    print(counters["extrfailcount"], " Extrenuous fails.")
    totalfails = counters["extrfailcount"] + counters["hashfailcount"] + counters["faileddelcount"] + counters["failedmovecount"]
    print(totalfails, " Fails in total.")
    totalsuccesses = counters["delcount"] + counters["movecount"]
    print(totalsuccesses, " Successes in total.")
    
        
def is_duplicate(file_hash, loaded_hashes):  # Now takes loaded_hashes
    """Checks if a hash is present in the loaded set."""
    return file_hash in loaded_hashes  # Efficient set lookup

def iterate_file(filepath, destination_folder, hash_file_p, file_extension, hashmem, counters):
    """Processes each file, handling potential filename collisions."""
    base, ext = os.path.splitext(filepath)  # Split filename and extension

    if ext.lower() != file_extension.lower():  # Case-insensitive extension comparison
        counters["skipcount"] += 1
        return 0 # Skip if extensions don't match
        
    folder_path, filename = os.path.split(filepath)
    pcname = os.path.basename(base)

    try:
        print("Calculating hash...")
        file_hash = calculate_file_hash(filepath)
        if file_hash is None:
            counters["hashfailcount"] += 1
            return 0 #skip if hash fails
        if is_duplicate(file_hash, hashmem):
            try:
                search_folder_flat(folder_path, pcname, None, counters, del_ass_file)  
                counters["hashsuccessescount"] += 1
                return 1
            except Exception as e:
                print(f"Unexpected error: {folder_path}: {e}")
                counters["extrfailcount"] += 1
                return 0
                
        else:
            try:
                base, ext = os.path.splitext(filename)  # Split filename and extension
                destination_path = os.path.join(destination_folder, base)

                counter = 1
                while (os.path.exists(destination_path)) and (os.path.isdir(destination_path)):  # Check for collisions
                    new_dirname = f"{base}({counter})" # Create new name
                    destination_path = os.path.join(destination_folder, new_dirname)
                    counter += 1
                try:
                    os.makedirs(destination_path)
                except Exception as e:
                    print(f"Failed to create destination directory: {e}")
                    counters["extrfailcount"] += 1
                    return 0
                
                search_folder_flat(folder_path, pcname, destination_path, counters, move_ass_file)

                hash_file_p.write(file_hash + "\n")
                hashmem.add(file_hash)
                counters["hashsuccessescount"] += 1
                return 1

            except Exception as e:
                print(f"Error moving {filepath} and associated files: {e}")
                counters["extrfailcount"] += 1
                return 0

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        counters["extrfailcount"] += 1
        return 0
    counters["extrfailcount"] += 1
    return 0
        
if __name__ == '__main__':
    source_folder = input("Enter the source directory: ")
    dest_folder = input("Enter the destination directory: ")
    file_ext = input("Enter the file extension(include dot): ")
    # Create destination folder if it doesn't exist
    if not os.path.exists(dest_folder):
        try:
            os.makedirs(dest_folder)
        except Exception as e:
            print(f"Error creating destination directory: {e}")
            print("Program will now quit.")
            raise SystemExit
    print("loading hash file...")
    try:
        hashvar = load_hashes_from_file(dest_folder)
    except Exception as e:
        print(f"Failed to read hash file: {e}")
        print("Program will now quit.")
        raise SystemExit
    hashfile = create_hash_file_handle(dest_folder)  # Use dest_folder here
    if hashfile is None:
        print("Error creating or opening hash file.")
        print("Program will now quit.")
        raise SystemExit
    print("Hash file loaded successfully.")
    search_folder(source_folder, hashfile, dest_folder, file_ext, hashvar, iterate_file)
    try:
        if hashfile:
            print("Closing hash file...")
            hashfile.close()
            print("Hash file closed successfully.")
    except Exception as e:
        print(f"Error closing hash file: {e}")