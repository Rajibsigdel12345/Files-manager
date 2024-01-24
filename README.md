# Files Manager
It is a simple program that makes use of os module

### Features
1. Manage Files in the given Folder by extension.
2. Ability to exclude any file extension to exclude.
3. Delete temporary files from default Temporary directory.
    > eg: **C:/Windows/Temp/**
4. Aditionally Delete files from folders.
5. Ability to exclude any file type from deleted.
6. Logs the action performed in the log files.

## Usage - OrganizeFiles Class

The `OrganizeFiles` class in the Files Manager Python Library provides functionality to organize files in a directory based on their extensions. This can help maintain a well-structured file system.

### Example

Consider the following example demonstrating how to use the `OrganizeFiles` class:

```python
from files_manager import OrganizeFiles

# Specify the path of the directory to organize
path = "/path/to/directory"

# Create an instance of the OrganizeFiles class
organizer = OrganizeFiles()
```
### Explanation
 - Import the OrganizeFiles class: Import the OrganizeFiles class from the files_manager library.

 - Specify the directory path: Set the path variable to the absolute path of the directory containing the files you want to organize.

 - Create an instance of OrganizeFiles: Instantiate the OrganizeFiles class to access its methods.

 - Organize files: Use the manage_by_extension method to organize files in the specified directory based on their extensions. The method will categorize files into predefined folders like Text Files, Image Files, Audio Files, Markup Files, Video Files, Spread Sheets, Powerpoint Files, and Miscellaneous.
#### Note
- The manage_by_extension method provides an interactive prompt to exclude specific file types from organization. It allows users to specify file extensions to be excluded from the organization process.

- The organization process creates new folders within the specified directory to categorize files based on their extensions.

- The log_action method from the parent FilesManager class is used to log actions such as folder creation and file movements.

## HandleTempFiles Class Usage

### Import the HandleTempFiles class
Import the `HandleTempFiles` class from the `files_manager` library.

```python
from files_manager import HandleTempFiles

# Define the list of temporary directories
temporary_dirs = ["C:/Users/ACER/AppData/Local/Temp/", "C:/Windows/Temp/", "C:/Windows/Prefetch/"]

# Create an instance of the HandleTempFiles class
temp_file_handler = HandleTempFiles(temporary=temporary_dirs)

# Delete temporary files in the specified temporary directories
temp_file_handler.delete_temp_files()

```
#### Note
- The delete_temp_files method prompts the user to specify the age of files to be deleted (in days) and whether to exclude any file types from deletion.

- Users can exclude specific file types by providing a comma-separated list of file extensions.

- The method performs a check on the specified temporary directories and identifies files older than the specified age for deletion.

- The log_action method from the parent FilesManager class is used to log actions such as file deletions and directory removals.


