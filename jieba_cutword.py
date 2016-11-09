import jieba
import sys
import os
import re
import jieba.posseg
from multiprocessing import Process

def split_jieba(line):
    seg_list = jieba.posseg.cut(line)
    ls = ""
    for w in seg_list:
        ls += w.word +':'+w.flag + ' '
    return ls

def read_and_write(file_name):
    line_list = []
    for line in open(file_name):
        lines = line.split(',')
        if len(lines) != 8:
            continue
        lines[3] = split_jieba(lines[3])
        line_list.append(','.join(lines))
    print line_list
    f = file("cut_"+file_name,'w')
    for i in line_list:
        f.write(i.encode('utf8'))
    f.close()

def func(file_list):
    print file_list
    for i in file_list:
        read_and_write(i)

if __name__ == '__main__':
    num = 4
    csv_files = []
    files = os.listdir("./")
    for i in files:
        if ".csv" not in i:
            continue 
        csv_files.append(i)
    file_dict = {}
    i = 0
    while i <= len(csv_files)/num+1:
        if (i+1)*len(csv_files)/num < len(csv_files):
            file_dict[i] = csv_files[i*len(csv_files)/num:(i+1)*len(csv_files)/num]
        else:
            file_dict[i] = csv_files[i*len(csv_files)/num:len(csv_files)]
        i += 1
    for k in file_dict.keys():
        file_list = file_dict.get(k)
        p = Process(target=func,args=(file_list,))
        p.start()
        p.join()
