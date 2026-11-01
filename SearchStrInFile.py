#FOR WINDOWS
import os

#This script does a case-insensitive, no wildcard search on
#the informed directory, printing filenames that contain
#the strings informed(separated by commas) in the filename
#or the content of the file(utf_8, utf_16_be and utf_16_le).

def get_user_input():
    """Gets the folder path and the search string from the user."""
    folder_path = input("Enter the folder path: ")
    if not folder_path:
        folder_path = os.path.dirname(os.path.abspath(__file__))
    search_string = input("Enter strings to search for separated by commas: ") # Encode to bytes for binary search
    return folder_path, search_string

def search_string_in_filename(filename, s):
    """Checks if the byte representation of the search string is present in the filename."""
    return s.upper() in filename.encode('utf_8').upper()

def search_string_in_binary_chunked(filepath, ss, chunk_size, overlap_size):
    """Checks if the byte representation of the search string is present in the binary file content by reading in overlapping chunks."""
    # try:
    with open(filepath, 'rb') as f:
        previous_chunk = b''
        while True:
            current_chunk = f.read(chunk_size)
            if not current_chunk:
                break
            combined_chunk = previous_chunk + current_chunk
            for sl in ss:
                for s in sl:
                    if s.upper() in combined_chunk.upper():
                        return True
            previous_chunk = current_chunk[-overlap_size:]
    return False


def process_file(filepath, ss, tam):
    """Processes a single binary file: checks filename and content for the byte representation of the search string."""
    filename = os.path.basename(filepath)

    for sl in ss:
        for s in sl:
            if search_string_in_filename(filename, s):
                print(filepath)
                return

    if search_string_in_binary_chunked(filepath, ss, 2**16, (tam*2)+16):
        print(filepath)
        return

def recursively_search_folder(folder_path, ss, tam):
    """Recursively searches the folder for files and processes them."""
    for root, _, files in os.walk(folder_path):
        for file in files:
            filepath = os.path.join(root, file)
            process_file(filepath, ss, tam)

def main():
    """Main function to get input and start the search."""
    folder_path, si = get_user_input()
    ssp = si.split(',')
    s8 = []
    s16le = []
    s16be = []
    for s in ssp:
        s8.append(s.encode('utf_8'))
        s16be.append(s.encode('utf_16_be'))
        s16le.append(s.encode('utf_16_le'))
    ss = [s8, s16be, s16le]
    tam = 0
    for sl in ss:
        for s in sl:
            curtam = len(s)
            if curtam > tam:
                tam = curtam
    recursively_search_folder(folder_path, ss, tam)

if __name__ == "__main__":
    main()
    input('Press enter to exit...')