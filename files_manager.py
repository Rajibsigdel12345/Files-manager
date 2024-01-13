import datetime
import glob
import os
import re
import shutil
import time
import numpy as np


class FilesManager():
    temporary_dirs = ["C:/Users/ACER/AppData/Local/Temp/",
                      "C:/Windows/Temp/", "C:/Windows/Prefetch/"]

    def __init__(self, temporary=0):
        """Add list of temporary files location you want to manipulate."""
        if temporary:
            self.temporary_dirs.extend(temporary)

    @classmethod
    def format_time(cls, date):
        """Converts time in seconds taken from epoch 1 Jan 1975 to current datetime objects
           \n Parameter
           date : int or float type
        """
        formatted_time = datetime.datetime.fromtimestamp(
            date).strftime('%Y-%m-%d %H:%M:%S')
        formatted_time = datetime.datetime.strptime(
            formatted_time, '%Y-%m-%d %H:%M:%S')
        return formatted_time

    def get_timediff(self, path):
        """Calculates time difference between present system time and given time of the Files present in given directory\n
           Parameter:\n
           \tpath: type string ; path of the file\n
           Returns tuple of (Difference time in days, Difference time in hours)
        """
        modified_time = os.path.getmtime(path)
        formatted_modified_time = self.format_time(modified_time)
        timediff = datetime.datetime.now()-formatted_modified_time
        time_in_hours = timediff.total_seconds()/(60*60)
        time_in_days = time_in_hours/24
        return time_in_days, time_in_hours

    def get_old_files(self, path, days, exclusion=False):
        """Identify files older than a specified number of days in a given directory.
           Parameters:
           path: str, path of the directory
           days: int, number of days to consider as old
           exclusion: list, file extensions to exclude
           Returns:
           list of old files
        """
        old_files = []
        files = np.array(glob.glob(os.path.join(path, '*')))
        if exclusion:
            for exclude in exclusion:
                files = list(
                    set(files) - set(glob.glob(os.path.join(path, f'*.{exclude}'))))

        for file in files:
            c = glob.glob(os.path.join(path, 'logs'))
            if file not in c:
                time_in_days, time_in_hours = self.get_timediff(file)
                if time_in_days > days:
                    old_files.append(file)
        return old_files

    def get_extension(self, path):
        """Get the base name and extension of files in a directory.
           Parameter:
           path: str, path of the directory
           Returns:
           list of [base, extension] pairs
        """
        extension = []
        files = np.array(os.listdir(path))
        for file in files:
            if os.path.isfile(os.path.join(path, file)):
                base, extend = os.path.splitext(file)
                extension.append([base, extend])
        return extension

    def print_old_files(self, files):
        """Print a list of old files."""
        for old_file in files:
            print(old_file)

    def log_action(self, info):
        """Log an action with the current date."""
        current_date = datetime.datetime.now()
        log_file_name = f'log-{current_date.year}-{current_date.month}-{current_date.day}.txt'
        log_path = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(log_path):
            os.mkdir(log_path)
            info = f'{log_path} Created'
            self.log_action(info)
        with open(os.path.join(log_path, log_file_name), '+a', encoding='utf-8') as log_file:
            log_file.write(f'{info}\n')


class OrganizeFiles(FilesManager):
    text_extension = ['.docx', '.doc', '.txt', '.pdf', '.md']
    image_extension = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.bmp']
    audio_extension = ['.mp3', '.wav']
    markup_extension = ['.html', '.xml', '.json', '.yaml', '.yml']
    video_extension = ['.avi', '.mp4']
    spread_sheet_extension = ['.xls', '.xlsx', '.csv']
    power_point_extension = ['.ppt', '.pptx']

    def __move(self, src, dist):
        try:
            shutil.move(src, dist)
            self.log_action(f'{src} moved to {dist}')
        except Exception as e:
            print(f'Error moving {src}: {e}')
            self.log_action(f'Error moving {src}: {e}')

    def manage_by_extension(self, path):
        extension = self.get_extension(path)
        new_path = ['Text Files', 'Image Files', 'Audio Files',
                    'Markup Files', 'Video Files', 'Spread Sheets', 'Powerpoint Files', 'Miscellaneous']

        # User input for exclusion
        flag = input(
            "\nDo you want to exclude any file type(s) to organize(Y/N): ").lower()
        exclude = set()
        if flag in ('y', 'yes'):
            exclude_input = input(
                "\nEnter extension(s) you want to exclude (comma-separated): ")
            exclude = set(['.' + ext.strip()
                          for ext in exclude_input.split(',')])

        for folder_name in new_path:
            folder_path = os.path.join(path, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                self.log_action(f'{folder_path} Created')

        for base, ext in extension:
            file_path = os.path.join(path, base + ext)
            print(file_path)
            destination_folder = None

            # Skip excluded extensions
            if ext in exclude:
                print(ext, exclude)
                continue

            for i, extensions_list in enumerate([self.text_extension, self.image_extension, self.audio_extension,
                                                self.markup_extension, self.video_extension, self.spread_sheet_extension,
                                                self.power_point_extension]):
                if ext in extensions_list:
                    destination_folder = os.path.join(path, new_path[i])
                    break

                destination_folder = os.path.join(path, new_path[-1])

            if destination_folder is not None:
                self.__move(file_path, destination_folder)


class HandleTempFiles(FilesManager):
    # ... (other methods)

    def __delete(self, info, old_file, type):
        try:
            if type == 'file':
                os.remove(old_file)
            elif type == 'directory':
                if len(os.listdir(old_file)) == 0:
                    os.rmdir(old_file)
                    self.log_action(info)
                else:
                    shutil.rmtree(old_file)
                    info = f'Files and Sub directory in {old_file} are deleted'
                    self.log_action(info)
        except OSError as e:
            print(f'Error deleting {old_file}: {e}')
            self.log_action(f'Error deleting {old_file}: {e}')

    def delete_temp_files(self):
        try:
            days = int(input("How old files to be deleted (days): \n"))
            flag = input(
                "Do you want to exclude any file type to be deleted (Y/N)?").lower()
            exclusion = []
            if flag in ("y", "yes"):
                exclusion_input = input(
                    "Enter the file extension type(s) you want to exclude (comma-separated):\n")
                exclusion = re.split('\s|,', exclusion_input)

            paths = self.temporary_dirs
            print(paths)
            old_file = [self.get_old_files(
                path, days, exclusion) for path in paths]
            old_file_path = np.array([])

            for old in old_file:
                old_file_path = np.append(old_file_path, old)

            print(old_file_path)

            if len(old_file_path) == 0:
                print("No files to be deleted.")
            else:
                print("Files being deleted:\n")
                self.print_old_files(old_file_path)

            temp = old_file_path.copy()

            while len(temp) > 0:
                confirm = input(
                    "\nDo you want to delete these files (Y/N)\n").upper()

                if confirm in ("Y", "YES"):
                    for old_file in old_file_path:
                        info = f'{old_file} is deleted'
                        if os.path.isfile(old_file):
                            self.__delete(info, old_file, "file")
                        elif os.path.isdir(old_file):
                            self.__delete(info, old_file, "directory")
                        temp = np.delete(temp, 0)
                    print("Files successfully deleted in:")
                elif confirm in ('N', "NO"):
                    print("Action cancelled!!!\n")
                    break
                else:
                    print("Invalid option.\n")
        except ValueError:
            print("Invalid input. Please enter a valid number for days.")


start = time.time()
files = HandleTempFiles()
files.delete_temp_files()
end = time.time()
print(f"{end - start} sec")
