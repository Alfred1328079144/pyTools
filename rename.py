
import os
def main():

    folder_name = input("请输入要重命名的文件夹:")
    name_file_name = input("请输入新名文件:")
    name_file_name = "C:/Users/v-chzh12/Desktop/namelist.txt"

    file_names = os.listdir(folder_name)
    name_file = open(name_file_name)
    namelist = name_file.readlines()
    i = 0
    while i<50:
        name = file_names[i]
        newname = namelist[i].strip()
        # old_file_name = "./" + folder_name + "/" + name
        # new_file_name = "./" + folder_name + "/" + str(i) + "[京东出品]-" + name1
        # os.rename(old_file_name, new_file_name)

        os.rename(str(folder_name + "/" + name),str(folder_name +"/"+ newname +".mp3"))
        i += 1
if __name__ == '__main__':
    main()