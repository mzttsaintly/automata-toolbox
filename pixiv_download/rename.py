# -*- encoding=utf8 -*-
__author__ = "ant"

import datetime
import os
import re
from tkinter import *
from tkinter.filedialog import askdirectory

curr_time = datetime.datetime.now()
curr_time.date()


def selectPath():
    path_ = askdirectory()
    chose_path.set(path_)


def ReName():
    path = chose_path.get()
    ext = name.get()
    os.chdir(path)
    # 常见的
    ext_list = [".jpg", ".png", ".jfif", ".webp", ".gif"]
    if ext:
        ext_list.append(f".{ext}")
    num = 1
    for file in os.listdir(path):
        # print(os.path.splitext(file)[-1]) #所有文件后缀
        # print(os.path.join(path,file)) #所有文件路径
        # print(file) #所有文件名
        if os.path.splitext(file)[-1] in ext_list:
            r_ext = os.path.splitext(file)[-1]
            if re.match('photo', file):
                pass
            else:
                os.rename(file, "photo_" + str(curr_time.date()) + "_" + str(num) + r_ext)
                num += 1


root = Tk()
root.title("根据后缀给文件排序")
chose_path = StringVar()
name = StringVar()
# name.set('jpg')

Label(root, text="目标路径：").grid(row=0, column=0)
Entry(root, textvariable=chose_path, state=DISABLED).grid(row=0, column=1)
Button(root, text="路径选择", command=selectPath).grid(row=0, column=2)

Label(root, text="r若有不常见文件后缀请输入：").grid(row=1, column=0)
Entry(root, textvariable=name).grid(row=1, column=1)
Button(root, text="批量重命名文件", command=ReName).grid(row=1, column=2)

Label(root, text="将以'photo_年-月-日_编号'的格式重命名指定后缀的文件").grid(row=2, column=1)

root.mainloop()
