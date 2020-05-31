import glob
import os
import re
import string


def main():
    filelist = []
    text_name = input("请输入要找的字符:")
    folder_name = input("请输入要找的目录:")

    print('%s\*.txt'%folder_name)
    file_names = glob.glob('%s\*.txt'%folder_name)

    for name in file_names:

        file = open(name,"r",encoding="UTF-16")
        lines = file.readlines()
        for line in lines:
            text = line.split("\t")
            if len(text)>1:
                if text[1].find(text_name)!=-1:
                    print(text[0])
        file.close()

if __name__ == '__main__':
    main()