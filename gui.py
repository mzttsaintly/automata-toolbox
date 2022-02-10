# from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename
import asyncio
from SqliteInImg.sqlite_link import *
from SqliteInImg.table import *

# python .\gui.py
# loop = asyncio.get_running_loop()
# 创建窗口
window = tk.Tk()
window.title('档案管理员')
window.geometry('600x500')
global img_png
db_name = tk.StringVar()
FileDirName = tk.StringVar()  # 文字变量储存
sqlite_host = "warfarin.db"


def start():
    """
    连接数据库
    :return: None
    """
    path_ = askopenfilename()
    db_name.set(path_)
    sqlite_host = db_name.get()
    print(f"{sqlite_host}")
    # loop = asyncio.get_running_loop()


def choose_dir():
    path_ = askdirectory()
    print(f"{path_}")
    FileDirName.set(path_)


def Batch_write():
    async def add_sqlite(table, img_name, character, work_name, tags, ero):
        print(f"{img_name}")
        # user_obj = table(img_name=img_name, character=character, work_name=work_name,tags=tags,ero=ero)
        # orm.add(table, user_obj)
        await engine.add(table,
                         {"img_name": img_name,
                          "character": character,
                          "work_name": work_name,
                          "tags": tags,
                          "ero": ero})

    asyncio.run(engine.create_all())
    # loop = asyncio.get_running_loop()
    path = FileDirName.get()
    # os.chdir(path)
    for file in os.listdir(path):
        # file_path = path + os.sep + file
        asyncio.run(add_sqlite(ImageInformation, file, "none", "none", "none", 0))


tk.Label(window, text="数据库名称：").grid(row=0, column=0)
tk.Entry(window, textvariable=db_name, state=tk.DISABLED).grid(row=0, column=1)
tk.Button(window, text="选择数据库", command=start).grid(row=0, column=2)

tk.Label(window, text="图片所在目录：").grid(row=1, column=0)
tk.Entry(window, textvariable=FileDirName, state=tk.DISABLED).grid(row=1, column=1)
tk.Button(window, text="选择图片目录", command=choose_dir).grid(row=1, column=2)

tk.Button(window, text="开始导入", command=Batch_write).grid(row=2, column=1)

window.mainloop()
# loop = asyncio.get_running_loop()
