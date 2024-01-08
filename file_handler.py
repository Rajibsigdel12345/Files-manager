
import os
save_path = "E:/Rajib/Python/learn python/Automation/dummy folder/"
for i in range(102):
    newpath = os.path.join(save_path + f'newfile{i}.ty')
    if not os.path.isfile(newpath):
        print(i)
        newfiles = open(newpath, '+w')
        newfiles.write(f"this is file{i}")
        newfiles.close()

# for i in range(len(os.listdir(save_path))):
#     file_path = os.path.join(save_path+f'newfile{i}.txt')
#     file = open(file_path, '+a')
#     file.write(f'/n new lines added to file{i}')
#     file.close()
