import os


def getFile(path):
    return os.listdir(path)
def main(path):
    idlistfile = open("C:/Users/v-chzh12/Desktop/id_Phoebe.txt")
    newfile = open("C:/Users/v-chzh12/Desktop/newidlist.txt","w")
    idlist = idlistfile.readlines()
    list = getFile(path)
    for filename in list:
        file = open(path + "/" + filename,encoding="UTF-16")
        lines = file.readlines()
        for line in lines:
            words = line.split("\t")
            if (str(int(words[0]))+"\n") in idlist:
                newfile.write(line)
        file.close()
    newfile.close()
    idlistfile.close()
if __name__ == '__main__':
    main("D:/workspace/data/process_data/Phoebe/txt")