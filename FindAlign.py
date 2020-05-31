import glob
import json
import os
import re
import shutil
import stat
import subprocess
import zipfile


def CopyFile(inputFilePath, outputFilePath):
    outputDir = os.path.dirname(outputFilePath)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    shutil.copyfile(inputFilePath, outputFilePath)
def FindAlignByFilelist(src_align, filelist, des_align):
    list_nowaves = []
    list_expected = []
    listaligns = []
    lines = open(filelist, 'r').readlines()
    for line in lines:
        line = line.strip('\n')
        if line not in list_expected:
            list_expected.append(line)
    files = glob.glob(src_align + r'\**\*.txt', recursive=True)
    for file in files:
        basename = os.path.basename(file)
        dir = os.path.dirname(file)
        id = basename.replace('.txt', '')
        if id in list_expected:
            CopyFile(file, os.path.join(dir.replace(src_align,des_align),basename))
            list_nowaves.append(id)
    x=list(set(list_expected).difference(set(list_nowaves)))
    print(x)
    print(len(x))


if __name__ == '__main__':
    src_align = input("请输入目标align目录：")
    filelist = input("请输入列表文件：")
    des_align = input("请输出目标align目录：")
    FindAlignByFilelist(src_align,filelist,des_align)