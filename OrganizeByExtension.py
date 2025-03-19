#FOR WINDOWS
import os
import shutil

#This script move the files to folders created in the same directory,
#each extension to its corresponding folder, without recursion.


def search_folder_flat(folder_path):
    """Searches only the specified folder (no subfolders) and processes files."""
    pcount = 0
    fcount = 0
    failc = 0
    try:
        for filename in os.listdir(folder_path):  # Use os.listdir()
            filepath = os.path.join(folder_path, filename)

            if os.path.isfile(filepath):  # Check if it's a file (not a directory)
                curstat = iterate_file(filepath)
                pcount += curstat
                fcount += 1
                if (curstat == 0):
                    failc += 1
                if (fcount % 100 == 0):
                    print(f"{fcount} files checked...")
                    print(f"{pcount} files processed...")
        print(f"{fcount} files checked.")
        print(f"{pcount} files processed.")
        print(f"{failc} files failed.")

    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
        return  # Or handle the error as you see fit
    except NotADirectoryError:
        print(f"Error: '{folder_path}' is not a directory.")
        return
    except Exception as e: # Catch other potential exceptions
        print(f"An unexpected error occurred: {e}")
        return

def iterate_file(filepath):
    """Moves a file to a folder named after its extension."""

    _, ext = os.path.splitext(filepath)
    ext = ext.lower()  # Case-insensitive

    if not ext:  # Skip files without extensions
        return 0

    try:
        # Create the destination folder if it doesn't exist
        dest_folder = os.path.join(os.path.dirname(filepath), ext[1:])  # Remove the leading dot from ext
        os.makedirs(dest_folder, exist_ok=True)

        # Move the file
        shutil.move(filepath, os.path.join(dest_folder, os.path.basename(filepath)))
        return 1  # Success

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return 0  # Failure
        
if __name__ == '__main__':
    source_folder = input("Enter the folder to search: ")
    search_folder_flat(source_folder)