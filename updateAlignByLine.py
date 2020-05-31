import os

def getFile(path):
    return os.listdir(path)


def main():

    oldpath = "D:/Tool/TTSData/ttsdataforCheckin/en-AU/Voices/SpeechOcean_F19/XmlScripts"
    newpath = "D:/workspace/data/process_data/SpeechOcean_F19/4_XmlScriptWithPron_AddDot"
    writepath = "C:/Users/v-chzh12/Desktop/1"
    list = getFile(oldpath)
    for filename in list:
        file = open(oldpath+"/"+filename,encoding="UTF-16")
        fileNew = open(newpath+"/"+filename,encoding="UTF-16")
        fileWrite = open(writepath + "/" + filename,"a+",encoding="UTF-16")
        lines = file.readlines()
        newlines = fileNew.readlines()
        i = 0
        if (len(lines)==len(newlines)):
            while i < len(lines):
                line = lines[i]
                newline = newlines[i]
                if("\"for\"" in line or "\"For\"" in line ):
                    fileWrite.write(newline)
                else:
                    fileWrite.write(line)
                i+=1
        else:
            print(filename)





if __name__ == '__main__':
    main()