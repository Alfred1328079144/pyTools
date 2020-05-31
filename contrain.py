import os
import codecs
def main():
  f = codecs.open(os.path.join(r"D:\workspace\CortanaNeural\esmxsrc\data\rename\rename", "train_norm.txt"), encoding="utf-8")
  fw = open(os.path.join(r"D:\workspace\CortanaNeural\esmxsrc\data\rename\rename", "metadata.txt"), 'w')
  lines = f.readlines()
  name = "Teresa"
  for line in lines:
    line = line.strip()
    eles = line.split("|")
    eles[0] = name + "_" + eles[0]
    fw.write("|".join(eles) + "\n")
  f.close()
  fw.close()
if __name__ == '__main__':
    main()