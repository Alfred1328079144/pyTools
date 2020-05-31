import os
from xml.dom.minidom import parse
import xml.dom.minidom
def findById(id,set):
    for dom in set:
        idNew = dom.getAttribute("id")
        if idNew == id:
            return dom
def findByWord(word,set):
    for dom in set:
        wNew = dom.getAttribute("v")
        if wNew == word:
            return dom
def getFile(path):
    return os.listdir(path)
def main(afterpath,beforepath,idset):
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    z = 0
    list = getFile(afterpath)
    flieIdList = open(idset,"w")
    for filename in list:
        file = open(afterpath+"/"+filename)
        fileNew = open(beforepath+"/"+filename)
        xNtype = os.path.splitext(file.name)
        x, type = xNtype
        if (type == ".xml"):
            DomTree = xml.dom.minidom.parse(file.name)
            DomTreeNew = xml.dom.minidom.parse(fileNew.name)
            collection = DomTree.documentElement
            collectionNew = DomTreeNew.documentElement
            sis = collection.getElementsByTagName("si")
            sisNew = collectionNew.getElementsByTagName("si")
            for si in sis:
                id = si.getAttribute("id")
                siNew = findById(id,sisNew)

                if siNew != None:
                    sent = si.getElementsByTagName("sent")[0]
                    sentNew = siNew.getElementsByTagName("sent")[0]
                    words = sent.getElementsByTagName("words")[0]
                    wordsNew = sentNew.getElementsByTagName("words")[0]
                    ws= words.getElementsByTagName("w")
                    wsNew= wordsNew.getElementsByTagName("w")
                    n = 0
                    while n<len(ws):
                        wNew = findByWord(ws[n].getAttribute("v"),wsNew)
                        if(wNew!=None):
                            if ws[n].getAttribute("p") != wNew.getAttribute("p"):

                                if ws[n].getAttribute("v")=="for":
                                    z += 1
                                    if ws[n].getAttribute("p") == "f . ax 1 . r" and wNew.getAttribute("p") == "f . oo 1":
                                        list1.append(id)
                                        flieIdList.write("1 %s\n"%(id))
                                        # editAlign(id,1)
                                    elif ws[n].getAttribute("p") == "f . oo 1 . r" and wNew.getAttribute("p") == "f . oo 1":
                                        list2.append(id)
                                        flieIdList.write("2 %s\n" % (id))
                                    elif ws[n].getAttribute("p") == "f . ax 1" and wNew.getAttribute("p") == "f . oo 1":
                                        list3.append(id)
                                        flieIdList.write("3 %s\n" % (id))
                                    elif ws[n].getAttribute("p") == "f . o 1 . r" and wNew.getAttribute("p") == "f . oo 1":
                                        list4.append(id)
                                        flieIdList.write("4 %s\n" % (id))
                                    elif ws[n].getAttribute("p") == "f . oo 1" and wNew.getAttribute("p") == "f . ax":
                                        list5.append(id)
                                        flieIdList.write("5 %s\n" % (id))
                                        editAlign(id,1)
                                    elif ws[n].getAttribute("p") == "f . ax 1 . r" and wNew.getAttribute("p") == "f . ax":

                                        flieIdList.write("6 %s\n" % (id))
                                    elif ws[n].getAttribute("p") == "f . oo 1 . r" and wNew.getAttribute("p") == "f . ax":

                                        flieIdList.write("7 %s\n" % (id))
                                    elif ws[n].getAttribute("p") == "f . ax 1" and wNew.getAttribute("p") == "f . ax":

                                        flieIdList.write("8 %s\n" % (id))
                                    else:
                                        print(id)
                                        print(ws[n].getAttribute("p"))
                                        print(wNew.getAttribute("p"))

                        n+=1
    print(z)

def editAlign(id,index):
    idname = id+".txt"
    if index == 1:
        for root, dirs, files in os.walk("D:/workspace/ForcedAlignment.Phone.NoSR", topdown=False):

            for name in files:
                if name == idname:
                    editedFile = open(os.path.join(root, name),"r")
                    writeFile = open(os.path.join(root, id+".bak"), "w")
                    lines = editedFile.readlines()
                    n = 0
                    while n < len(lines):

                        word = lines[n].split(" ")
                        if word[1] == "oo\n":
                            beforeword = lines[n-1].split(" ")[1]
                            if beforeword == "f\n":

                                word[1] = word[1].replace("oo","ax")

                                writeFile.write(word[0]+" "+word[1])
                        else:
                            writeFile.write(lines[n])
                        n+=1

                    editedFile.close()
                    writeFile.close()
                    os.remove(os.path.join(root, name))
                    os.rename("%s.bak" %os.path.join(root, id),os.path.join(root, name))
    if index == 2:
        for root, dirs, files in os.walk("C:/Users/v-chzh12/Desktop/1", topdown=False):
            for name in files:
                if name == id:
                    editedFile = open(os.path.join(root, name))
                    lines = editedFile.readlines()
                    n = 0
                    while n < len(lines):
                        word = lines[n].split(" ")
                        if word[1] == "ax":
                            beforeword = lines[n-1].split(" ")[1]
                            if beforeword == "f":
                                word[1].replace("ax","oo")
                        n+=1
if __name__ == '__main__':
    afterpath = input("原目录")
    beforepath = input("新目录")
    idset = input("id目录")
    idset = "C:/Users/v-chzh12/Desktop/id.txt"
    main(afterpath,beforepath,idset)
