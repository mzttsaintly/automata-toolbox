import tkinter as tk
from tkinter.filedialog import askdirectory
import os


def get_dir():
    path_ = askdirectory()
    FileDirName.set(path_)

window = tk.Tk()
window.title('档案管理员')
window.geometry('600x500')
global img_png
db_name = tk.StringVar()
FileDirName = tk.StringVar()  # 文字变量储存
sqlite_host = "warfarin.db"
tk.Label(window, text="数据库名称：").grid(row=0, column=0)
tk.Entry(window, textvariable=db_name, state=tk.DISABLED).grid(row=0, column=1)
tk.Button(window, text="选择数据库").grid(row=0, column=2)

tk.Label(window, text="图片所在目录：").grid(row=1, column=0)
tk.Entry(window, textvariable=FileDirName, state=tk.DISABLED).grid(row=1, column=1)
tk.Button(window, text="选择图片目录").grid(row=1, column=2)

tk.Button(window, text="开始导入").grid(row=2, column=1)

# window.mainloop()
