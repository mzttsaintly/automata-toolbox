import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.filedialog import askdirectory


def get_dir():
    path_ = askdirectory()
    FileDirName.set(path_)

global img_png
ero_list = ["1", "2", "3"]
ero_library = tk.Tk()
ero_library.title('档案管理员')
ero_library.geometry('1080x500')
ero_img_name = tk.StringVar()
ero_path_name = tk.StringVar()
ero_character = tk.StringVar()
ero_title = tk.StringVar()
ero_hair = tk.StringVar()
ero_tags = tk.StringVar()
ero_ero = tk.IntVar()
db_name = tk.StringVar()
FileDirName = tk.StringVar()  # 文字变量储存
sqlite_host = "warfarin.db"
ero_in_frame = tk.Frame(ero_library)
ero_out_frame = tk.Frame(ero_library)
ero_show_frame = tk.Frame(ero_library)

# 区域布局
ero_in_frame.pack(side="left")
ero_out_frame.pack(side="left")
ero_show_frame.pack(side="right")

# ero_in_frame 将图片导入数据库
tk.Label(ero_in_frame, text="向数据库批量导入图片并初始化").grid(row=3, column=1)

tk.Label(ero_in_frame, text="数据库名称：").grid(row=0, column=0)
tk.Entry(ero_in_frame, textvariable=db_name, state=tk.DISABLED).grid(row=0, column=1)
tk.Button(ero_in_frame, text="选择数据库").grid(row=0, column=2)

tk.Label(ero_in_frame, text="图片所在目录：").grid(row=1, column=0)
tk.Entry(ero_in_frame, textvariable=FileDirName, state=tk.DISABLED).grid(row=1, column=1)
tk.Button(ero_in_frame, text="选择图片目录").grid(row=1, column=2)

tk.Button(ero_in_frame, text="开始导入").grid(row=2, column=1)

# ero_out_frame 显示所选图片信息
tk.Label(ero_out_frame, text="显示并修改图片信息").grid(row=0, column=1)
tk.Label(ero_out_frame, text="图片文件名：").grid(row=1, column=0)
tk.Entry(ero_out_frame, textvariable=ero_img_name, state=tk.DISABLED).grid(row=1, column=1)
tk.Label(ero_out_frame, text="图片所在文件夹：").grid(row=2, column=0)
tk.Entry(ero_out_frame, textvariable=ero_path_name, state=tk.DISABLED).grid(row=2, column=1)
tk.Label(ero_out_frame, text="图片中的角色：").grid(row=3, column=0)
tk.Entry(ero_out_frame, textvariable=ero_character).grid(row=3, column=1)
tk.Label(ero_out_frame, text="角色来源作品名：").grid(row=4, column=0)
tk.Entry(ero_out_frame, textvariable=ero_title).grid(row=4, column=1)
tk.Label(ero_out_frame, text="角色头发：").grid(row=5, column=0)
tk.Entry(ero_out_frame, textvariable=ero_hair).grid(row=5, column=1)
tk.Label(ero_out_frame, text="其他图片标签：").grid(row=6, column=0)
tk.Entry(ero_out_frame, textvariable=ero_tags).grid(row=6, column=1)
tk.Label(ero_out_frame, text="主观ero度：").grid(row=7, column=0)
tk.Entry(ero_out_frame, textvariable=ero_ero).grid(row=7, column=1)
tk.Label(ero_out_frame, text="选择图片：").grid(row=8, column=0)
combo = ttk.Combobox(ero_out_frame, values=ero_list, width=17)
combo.grid(row=8, column=1)
tk.Button(ero_out_frame, text="打开图片").grid(row=8, column=2)
tk.Button(ero_out_frame, text="上一张", width=10).grid(row=9, column=0)
tk.Button(ero_out_frame, text="下一张", width=10).grid(row=9, column=1)
tk.Button(ero_out_frame, text="确认修改").grid(row=10, column=1)

# ero_show_frame 显示所选图片
tk.Label(ero_show_frame, text="显示所选图片").grid(row=0, column=1)
img_png = r"D:\automata-toolbox\test_img\00101.jpg"
img_open = Image.open(img_png).resize((480, 268))
# img_open = Image.open(img_png)
img_open_PIL = ImageTk.PhotoImage(img_open)
ero_show = tk.Label(ero_show_frame, image=img_open_PIL)
ero_show.grid(row=1, column=1)

# def changeSize(event):
#     image = ImageTk.PhotoImage(img_open.resize((event.width, event.height), Image.ANTIALIAS))
#     # ero_show['image'] = image
#     ero_show.image = image
#
# ero_show.bind('<Configure>', changeSize)


ero_library.mainloop()
