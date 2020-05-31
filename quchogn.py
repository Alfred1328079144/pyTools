file_list = []  #创建一个空列表
def out_file():
    #file_2 = open_file()
    file = "D:/workspace/data/eses_newdata/phone_seq.txt"    #打开需要去重的文件
    with open(file, "r", encoding="utf-8") as f:
        file_2 = f.readlines()
        out_file=set(file_2)
        print(len(out_file))
        f.close()
    with open(file, "r", encoding="utf-8") as fn:
        x_2 = fn.readlines()
        a = 0
        with open("D:/workspace/data/eses_newdata/new_phone_seq.txt", "a+", encoding="utf-8") as f:
            for x in x_2:
                if x in out_file:
                    out_file.remove(x)
                    f.write(x)
                else:
                    a+=1
                    print(x)
            print(a)
            f.close()
            fn.close()
if __name__ =="__main__":
    out_file()