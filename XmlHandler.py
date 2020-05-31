import os
from xml.dom.minidom import parse
import xml.dom.minidom

def getFile(path):
    return os.listdir(path)


if __name__ == '__main__':
    saveSet = set()
    path = "D:/testFolder"
    list = getFile(path)
    newFile = open("D:/workspace/result/new.txt","w",encoding="utf-16")
    for filename in list:
        print(path+"/"+filename)
        file = open(path+"/"+filename)
        xNtype = os.path.splitext(file.name)
        x,type = xNtype
        if(type==".xml"):
            DomTree = xml.dom.minidom.parse(file.name)
            count = len(DomTree.documentElement.getElementsByTagName("text"))
            x=0;
            while x<count:

                text = DomTree.documentElement.getElementsByTagName("text")[x].childNodes[0].data.strip()
                if text not in saveSet:
                    saveSet.add(text)
                    newFile.write(text+"\n")
                x += 1

