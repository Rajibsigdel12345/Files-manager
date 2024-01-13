
import os
save_path = "E:/Rajib/Python/learn python/Automation/dummy folder/"
for i in range(102):
    newpath = os.path.join(save_path + f'newfile{i}.nw')
    if not os.path.isfile(newpath):
        print(i)
        with open(newpath, '+w') as newfiles:
            newfiles.write(f"this is file{i}")

# for i in range(len(os.listdir(save_path))):
#     file_path = os.path.join(save_path+f'newfile{i}.txt')
#     file = open(file_path, '+a')
#     file.write(f'/n new lines added to file{i}')
#     file.close()
