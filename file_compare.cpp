//FOR WINDOWS

//This code compiles on MinGW and serves as the executable for the 
//function of having an option on the on-right-click menu of Windows
//Explorer called "compare files". Selecting 2 files via Windows Ex-
//plorer, right-clicking them and selecting "compare files", lets you
//know if 2 files are equal or different in content.

//Compile the code using the following command:
//g++ file_compare.cpp -o file_compare.exe -static-libgcc -static-libstdc++ -lshlwapi -mwindows

//Save the executable in a location of your preference and install it
//to the system registry so it can appear as an option at the Explorer
//menu. A install.reg file must be created like this:

/*

Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\*\shell\CompareFiles]
@="Compare Files"

[HKEY_CLASSES_ROOT\*\shell\CompareFiles\command]
@="\"X:\\path_to_exe\\file_compare.exe\" \"%L\""

*/

//You should replace X with your drive letter and path_to_exe with the 
//path where your file_compare.exe is located, always escaping the backslashes
//with another backslash.


#include <windows.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <shlwapi.h> // For PathFileExists

#pragma comment(lib, "shlwapi.lib") // Link with shlwapi.lib

int compareFiles(const std::string& filePath1, const std::string& filePath2) {
    std::ifstream file1(filePath1, std::ios::binary | std::ios::ate); // Open in binary and at the end
    std::ifstream file2(filePath2, std::ios::binary | std::ios::ate);

    if (!file1.is_open() || !file2.is_open()) {
        return 0; // Error opening files
    }

    std::streamsize size1 = file1.tellg(); // Get file sizes
    std::streamsize size2 = file2.tellg();

    if (size1 != size2) {
        return -1; // Files have different sizes
    }

    file1.seekg(0, std::ios::beg); // Reset file pointers to the beginning
    file2.seekg(0, std::ios::beg);

    std::vector<char> buffer1(4096);
    std::vector<char> buffer2(4096);

    while (true) {
        file1.read(buffer1.data(), buffer1.size());
        file2.read(buffer2.data(), buffer2.size());

        std::streamsize count1 = file1.gcount();
        std::streamsize count2 = file2.gcount();

        if (count1 != count2) {
			file1.close();
			file2.close();
            return -1; // Different sizes or different content
        }

        if (count1 == 0) {
			file1.close();
			file2.close();
            return 1; // End of files, and they were equal
        }

        if (memcmp(buffer1.data(), buffer2.data(), count1) != 0) {
			file1.close();
			file2.close();
            return -1; // Different content
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc == 2) {
        HKEY hKey;
        DWORD dwDisposition;
        const char* regKeyPath = "Software\\PhillFileCompare"; // Registry key path

        if (RegCreateKeyExA(HKEY_CURRENT_USER, regKeyPath, 0, NULL, REG_OPTION_NON_VOLATILE, KEY_READ | KEY_WRITE, NULL, &hKey, &dwDisposition) == ERROR_SUCCESS) {

            char firstFilePath[MAX_PATH];
            DWORD firstFilePathSize = sizeof(firstFilePath);
			
			
			
	        std::string filePath1;
            std::string filePath2 = argv[1];
			std::string msg_str;
			

            if (RegGetValueA(hKey, NULL, "FirstFilePath", RRF_RT_REG_SZ, NULL, firstFilePath, &firstFilePathSize) == ERROR_SUCCESS) { // First file already selected
				int _res = compareFiles(firstFilePath, argv[1]);
				switch (_res) {
					case (0):
					    
						MessageBoxA(NULL, "Error reading file.", "Error", MB_OK | MB_ICONERROR);
						break;
						
					case (-1):
						filePath1 = firstFilePath;
						msg_str = "Files are different.\n"+filePath2+"\n"+filePath1;
						MessageBoxA(NULL, msg_str.c_str(), "Comparison Result", MB_OK | MB_ICONWARNING);
					    break;
					case (1):
						filePath1 = firstFilePath;
						msg_str = "Files are equal.\n"+filePath2+"\n"+filePath1;
						MessageBoxA(NULL, msg_str.c_str(), "Comparison Result", MB_OK | MB_ICONINFORMATION);
						break;
				}
				
				
				


                RegDeleteValueA(hKey, "FirstFilePath"); // Delete registry value
            } else { // First file selection
                RegSetValueExA(hKey, "FirstFilePath", 0, REG_SZ, (const BYTE*)argv[1], (strlen(argv[1]) + 1) * sizeof(char));
            }

            RegCloseKey(hKey);
        } else {
            MessageBoxA(NULL, "Error accessing registry.", "Error", MB_OK | MB_ICONERROR);
        }

        return 0;
    } else {
        MessageBoxA(NULL, "Only one argument allowed.", "Error", MB_OK | MB_ICONERROR);
        return 1;
    }
}
