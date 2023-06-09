import re
import os
import loguru

from tkinter import *
from tkinter.filedialog import askdirectory

log = loguru.logger

link_pattern = re.compile('src="(.*?)"')


def selectPath():
    path_ = askdirectory()
    chose_path.set(path_)


def get_src(file):
    with open(file, 'r', encoding='utf-8') as f:
        res = f.read()
        res_list = re.findall(link_pattern, res)
        # new_res = make_obj(res_list)
        new_res_dict = make_obj_dict(res_list)
        new_res = dict_to_list(new_res_dict)
        # f.close()
        file_data = ""
        with open(file, 'r', encoding='utf-8') as rf:
            for line in rf:
                for key, value in new_res_dict.items():
                    if value in line:
                        line = line.replace(value, key)
                file_data += line
        log.debug(file_data)
        with open(file, 'w', encoding='utf-8') as wf:
            wf.write(file_data)

    with open(file, 'r', encoding='utf-8') as ft:
        res = ft.read()
        content_add = "\r".join(new_res)
        # log.debug(content_add)
        pos = res.find('<script>')
        if pos == -1:
            pos = res.find('<script setup>')
            if pos != -1:
                with open(file, 'w', encoding='utf-8') as f2:
                    res = res[:pos + 14] + content_add + res[pos + 14:]
                    f2.write(res)
        elif pos != -1:
            with open(file, 'w', encoding='utf-8') as f2:
                res = res[:pos + 8] + content_add + res[pos + 8:]
                f2.write(res)


def make_obj(res_list):
    new_res = []
    for i in range(len(res_list)):
        new_res.append(f'const img{str(i).rjust(3, "0")} = \'{res_list[i]}\'')
    log.debug(new_res)
    return new_res


def make_obj_dict(res_list):
    new_res_dict = {}
    for i in range(len(res_list)):
        new_res_dict[f'img{str(i).rjust(3, "0")}'] = f'{res_list[i]}'
    # log.debug(new_res_dict)
    return new_res_dict


def dict_to_list(new_res_dict: dict):
    new_res = []
    for key, value in new_res_dict.items():
        new_res.append(f'const {key} = \'{value}\'')
    log.debug(new_res)
    return new_res


def get_dir(path_name):
    os.chdir(path_name)
    print(path_name)
    for file in os.listdir(path_name):
        log.debug(file)
        if os.path.splitext(file)[-1] == ".vue":
            get_src(file)


def tk_get_dir():
    true_path = chose_path.get()
    log.debug(true_path)
    get_dir(true_path)


root = Tk()
root.title("批量处理vue图片链接")
chose_path = StringVar()

Label(root, text="目标路径：").grid(row=0, column=0)
Entry(root, textvariable=chose_path, state=DISABLED).grid(row=0, column=1)
Button(root, text="路径选择", command=selectPath).grid(row=0, column=2)
Button(root, text="开始", command=tk_get_dir).grid(row=0, column=3)

root.mainloop()
