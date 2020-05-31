import os
import codecs
def main():
  wavs = os.listdir("mels")
  f = codecs.open("D:/workspace/CortanaNeural/esmxsrc/data/rename/mels/train_norm.txt", encoding="utf-8")
  lines = f.readlines()
  fw = codecs.open("D:/workspace/CortanaNeural/esmxsrc/data/rename", 'w', encoding="utf-8")
  for l in lines:
    l = l.strip()
    id = l.split("|")[0]
    if id in wavs:
      # print(id)
      fw.write(l + "\n")
  f.close()
  fw.close()
if __name__ == '__main__':
    main()