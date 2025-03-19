#FOR WINDOWS
import os
import shutil
import subprocess

#This script attempts to remove empty directories and sub-
#directories from informed folder without creating long lists 
#or consuming a lot of resources.

def remove_directory_(dir_path, depth):
    """Removes a directory, handling exceptions and retrying."""

    if depth > 2:
        return False  # Stop recursion at max depth

    try:
        shutil.rmtree(dir_path)
        return True  # Success

    except FileNotFoundError:
        return True # Directory already deleted
    except Exception as e:
        try:
            # Try command-line deletion
            subprocess.run(["rmdir", "/s", "/q", dir_path], check=True) # /s: subdirectories, /q: quiet
            return True # Success after cmd line

        except Exception as e:
            try:
                # Remove read-only attributes and try again
                subprocess.run(["attrib", "-r", dir_path], check=True)
                for root, dirs, files in os.walk(dir_path):
                    for name in dirs:
                        dirpath = os.path.join(root, name)
                        subprocess.run(["attrib", "-r", dirpath], check=True)
                return remove_directory_(dir_path, depth + 1) # Retry with increased depth
            except Exception as e:
                print(f"Failed to remove attributes: {e}")
                return remove_directory_(dir_path, depth + 1)
        



def search_folder_flat(folder_path, counters):
    """Recursively searches the specified folder and processes directories."""

    try:
        for filename in os.listdir(folder_path):  # Use os.listdir()
            filepath = os.path.join(folder_path, filename)

            if os.path.isdir(filepath): 
                counters["totalcount"] += 1
                try:
                    if is_folder_empty(filepath):
                        if remove_directory_(filepath, 0):
                            counters["delcount"] += 1
                            print(f"Deleted: {filepath}")
                        else:
                            counters["faileddelcount"] += 1
                            print(f"Failed to delete: {filepath}")
                    else:
                        counters["skipcount"] += 1
                        search_folder_flat(filepath, counters)
                except:
                    counters["extrfailcount"] += 1
                    print(f"Failed to check if folder is empty: {filepath}")
                ntemp = counters["totalcount"]
                if(ntemp % 100 == 0):
                    print(f"{ntemp} objects processed...")
          
    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
          # Or handle the error as you see fit
        counters["fatalfails"] += 1
        raise Exception("failed to search root folder.")
    except NotADirectoryError:
        print(f"Error: '{folder_path}' is not a directory.")
        counters["fatalfails"] += 1
        raise Exception("failed to flat search folder.")
    except Exception as e: # Catch other potential exceptions
        print(f"failed to flat search folder: {folder_path}, {e}")
        counters["fatalfails"] += 1
        raise Exception("failed to flat search folder")
    

 

   
def is_folder_empty(folder_path):
    """Recursively searches for files in a folder and its subfolders"""
    for root, _, files in os.walk(folder_path):  # os.walk() for recursive traversal
        for filename in files:
            filepath = os.path.join(root, filename)  # Full path to the file
            if os.path.isfile(filepath):  
                return False 
    return True   
    
if __name__ == '__main__':
    source_folder = input("Enter the directory to search: ")
    counters = {  # Initialize all counters to 0
        "totalcount": 0,
        "delcount": 0,
        "skipcount": 0,
        "faileddelcount": 0,
        "extrfailcount": 0,
        "fatalfails": 0,
    }    
   
    search_folder_flat(source_folder, counters)
    print(counters["totalcount"], " objects checked.")
    print(counters["delcount"], " Deletion successes.")
    print(counters["skipcount"], " Skips.")
    print(counters["faileddelcount"], " Deletion fails.")
    print(counters["extrfailcount"], " Extrenuous fails.")
    print(counters["fatalfails"], " Fatal fails.")
    totalfails = counters["extrfailcount"] + counters["faileddelcount"]
    print(totalfails, " Fails in total.")
    
    