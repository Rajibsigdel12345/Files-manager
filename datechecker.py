
import datetime
import glob
import os
import shutil
import time


from sympy import true


class FilesManager():
    temporary_dirs = ["C:/Windows/SoftwareDistribution/Download/",
                      "C:/Users/ACER/AppData/Local/Temp/", "C:/Windows/Temp/"]

    def __init__(self, temporary=0):
        "Add list of temporary files location you want to manipulate."
        if temporary:
            self.temporary_dirs.extend(temporary)

    @classmethod
    def format_time(cls, date):
        """Converts time in seconds taken from epoh 1 Jan 1975 to current datetime objects
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

    def get_old_files(self, path, days):
        old_files = []
        for files in os.listdir(path):
            c = glob.glob(f'{path}logs')
            if path+files not in c:
                time_in_days, time_in_hours = self.get_timediff(path+files)
                if time_in_days > days:
                    old_files.append(path+files)
        return old_files

    def get_extension(self, path):
        extension = []
        files = os.listdir(path)
        for file in files:
            if os.path.isfile(path+file):
                base, extend = os.path.splitext(file)
                extension.append([base, extend])
        return extension

    def print_old_files(self, path):
        for old_file in path:
            print(old_file)

    def log_action(self, info, path):
        current_date = datetime.datetime.now()
        log_file_name = f'log-{current_date.year}-{current_date.month}-{current_date.day}.txt'
        log_path = path+"logs/"
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        log_file = open(f'{log_path}{log_file_name}', '+a')
        log_file.write(f'{info}'+"\n")
        log_file.close()


class OrganizeFiles(FilesManager):
    text_extension = ['.docx', '.doc', '.txt', '.pdf', '.md']
    image_extension = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.bmp']
    audio_extension = ['.mp3', '.wav']
    markup_extension = ['.html', '.xml', '.json', '.yaml', '.yml']
    video_extension = ['.avi', '.mp4',]
    spread_sheet_extension = ['.xls', '.xlsx', '.csv']
    power_point_extension = ['.ppt', '.pptx']

    def __move(self, src, dist, path):
        try:
            shutil.move(src, dist)
            self.log_action(f'{src} moved to {dist}', path)
        except Exception as e:
            print(f'{e}')
            self.log_action(e, path)

    def manage_by_extension(self, path):
        extension = self.get_extension(path)
        new_path = ['Text Files', 'Image Files', 'Audio Files',
                    'Markup Files', 'Video Files', 'Spread Sheets', 'Powerpoint Files']
        for i in range(len(new_path)):
            if not os.path.exists(path+new_path[i]):
                os.makedirs(path+new_path[i])
            new_path[i] = path+new_path[i]
        print(new_path)
        for x in extension:
            z = "".join(x)
            if x[1] in self.text_extension:
                self.__move(path+z, new_path[0], path)
            elif x[1] in self.image_extension:
                self.__move(path+z, new_path[1], path)
            elif x[1] in self.audio_extension:
                self.__move(path+z, new_path[2], path)
            elif x[1] in self.markup_extension:
                self.__move(path+z, new_path[3], path)
            elif x[1] in self.video_extension:
                self.__move(path+z, new_path[4], path)
            elif x[1] in self.spread_sheet_extension:
                self.__move(path+z, new_path[5], path)
            elif x[1] in self.power_point_extension:
                self.__move(path+z, new_path[6], path)


class HandleTempFiles(FilesManager):
    def __delete(self, info, old_file, type, path):
        try:
            if type == 'file':
                os.remove(old_file)
            elif type == 'directory':
                os.rmdir(old_file)
            self.log_action(info, path)
        except OSError as e:
            print(e)
            self.log_action(e, path)

    def delete_temp_files(self):
        days = int(input("How old files to be deleted (days): \n"))
        paths = self.temporary_dirs
        for path in paths:
            old_file_path = self.get_old_files(path, days)
            if len(old_file_path) == 0:
                print("No Files to be deleted")
            else:
                print("Files being deleted\n")
            self.print_old_files(old_file_path)
            temp = old_file_path.copy()
            while len(temp) > 0:
                confirm = input(
                    "\nDo you wand to delete these files (Y/N)\n").upper()
                if (confirm == "Y" or confirm == "YES"):
                    for old_file in old_file_path:
                        info = f'{old_file} is deleted'
                        if os.path.isfile(old_file):
                            self.__delete(info, old_file, "file", path)
                        elif os.path.isdir(old_file):
                            self.__delete(info, old_file, "directory", path)
                        temp.pop(0)
                elif confirm == "N" or confirm == "NO":
                    print("Action Cancelled!!!\n")
                    break
                else:
                    print("Invalid option.\n")


start = time.time()
# file = OrganizeFiles(
#     ["E:/Rajib/Python/learn python/Automation/dummy folder/", "E:/Music/"])
# print(file.manage_by_extension(
#     "E:/Rajib/Python/learn python/Automation/dummy folder/"))

file2 = HandleTempFiles()
file2.delete_temp_files()

end = time.time()
print(end-start)
