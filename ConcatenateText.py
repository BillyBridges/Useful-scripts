#FOR WINDOWS
import pathlib

# Concatenates text from multiple files into one file.

def concatenate_files():
    # 1. Get user inputs
    folder_input = input("Enter the folder path to search: ").strip()
    extension = input("Enter the file extension (e.g., .txt, .py): ").strip()
    output_filename = input("Enter the name for the output file (e.g., combined.txt): ").strip()

    # Ensure extension starts with a dot
    if not extension.startswith('.'):
        extension = '.' + extension

    folder_path = pathlib.Path(folder_input)
    output_path = pathlib.Path(output_filename)

    # 2. Validate folder path
    if not folder_path.is_dir():
        print(f"Error: The path '{folder_input}' is not a valid directory.")
        return

    try:
        # 3. Open output file for writing
        with open(output_path, 'w', encoding='latin-1') as outfile:
            found_files = False
            
            # 4. Recursively find files
            for file_path in folder_path.rglob(f"*{extension}"):
                # Prevent the script from reading its own output file if it's in the same folder
                if file_path.resolve() == output_path.resolve():
                    continue
                
                found_files = True
                print(f"Processing: {file_path.name}")

                try:
                    with open(file_path, 'r', encoding='latin-1', errors='replace') as infile:
                        # Write the header
                        outfile.write(f"***Begin({file_path.name})***\n")
                        
                        # Write file content
                        outfile.write(infile.read())
                        
                        # Ensure there's a newline before the footer
                        if not outfile.tell() or outfile.write('\n'): pass 
                        
                        # Write the footer
                        outfile.write(f"\n***End({file_path.name})***\n\n")
                
                except Exception as e:
                    print(f"Could not read {file_path.name}: {e}")

            if found_files:
                print(f"\nSuccess! All files have been concatenated into '{output_filename}'.")
            else:
                print(f"\nNo files with extension '{extension}' were found.")

    except Exception as e:
        print(f"An error occurred while creating the output file: {e}")

if __name__ == "__main__":
    concatenate_files()