import os
from xml.dom.minidom import parse
import xml.dom.minidom
def getFile(path):
    return os.listdir(path)
def filter():
    set = []
    idfile = open("C:/Users/v-chzh12/Desktop/id.txt")
    lines = idfile.readlines()
    for line in lines:
        map = line.split(" ")
        set.append(map[1].strip()+".txt")
    idfile.close()
    return set
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
def main():
    beforepath = "D:/workspace/data/process_data/SpeechOcean_F19/4_XmlScriptWithPron_AddDot"
    afterpath = "D:/Tool/TTSData/ttsdata0518/en-AU/Voices/SpeechOcean_F19/XmlScripts"
    list = getFile(afterpath)
    for filename in list:
        file = open(afterpath+"/"+filename,encoding="UTF-16")
        fileNew = open(beforepath+"/"+filename,encoding="UTF-16")
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
                                    ws[n].setAttribute("p",wNew.getAttribute("p"))

                        n+=1
            writefile = open("C:/Users/v-chzh12/Desktop/1/%s"%filename,"a+",encoding="UTF-16")
            DomTree.writexml(writefile,indent='',addindent='',newl='',encoding='UTF-16')

if __name__ == '__main__':
    main()
