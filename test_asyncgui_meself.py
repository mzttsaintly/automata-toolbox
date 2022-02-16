import asyncio
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from EroLibrary.erolibrary import AsyncEngine, AsyncORM
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import select, and_


class App(tk.Tk):

    def __init__(self, app_loop, interval=1 / 120):
        super(App, self).__init__()
        self.loop = app_loop
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.title('EroLibrary')
        self.geometry('1080x500')
        self.ero_id = 1
        self.ero_img_name = tk.StringVar()
        self.ero_path_name = tk.StringVar()
        self.ero_character = tk.StringVar()
        self.ero_title = tk.StringVar()
        self.ero_hair = tk.StringVar()
        self.ero_tags = tk.StringVar()
        self.ero_ero = tk.IntVar()
        self.ero_list = ["1"]

        self.db_name = tk.StringVar()
        self.FileDirName = tk.StringVar()  # 文字变量储存
        self.img_png = r"D:\automata-toolbox\test_img\00101.jpg"
        # self.img_png = f"{self.FileDirName.get() + self.ero_list[0]}"
        self.img_open = Image.open(self.img_png).resize((480, 268))
        self.img_open_pil = ImageTk.PhotoImage(self.img_open)
        self.tasks = []
        self.tasks.append(app_loop.create_task(self.sqlite_link()))
        self.tasks.append(app_loop.create_task(self.gui_in(app_loop)))
        self.tasks.append(app_loop.create_task(self.gui_out(app_loop)))
        self.tasks.append(app_loop.create_task(self.gui_show(app_loop)))
        self.tasks.append(app_loop.create_task(self.updater(interval)))

    async def sqlite_link(self):
        print("输入数据库名字（非根目录下需输入完整路径）")
        sqlite_host = input()
        print("输入图片文件夹路径（绝对路径）")
        img_path = input()
        print(f"数据库：{sqlite_host}\n文件夹：{img_path}")
        self.db_name.set(f"{sqlite_host}")
        self.FileDirName.set(f"{img_path}")
        global engine, Base
        engine = AsyncORM(f"sqlite+aiosqlite:///{sqlite_host}")
        Base = engine.Base
        await engine.create_all()

    async def Batch_write(self):
        await engine.create_all()

        class ImageInformation(Base):
            __table_args__ = {'extend_existing': True}
            __tablename__ = "image_information"
            id = Column(Integer, primary_key=True, autoincrement=True)
            img_name = Column(String(32))
            path_name = Column(String(32))
            character = Column(String(32))
            title = Column(String(32))
            hair = Column(String(32))
            tags = Column(String(32))
            ero = Column(Integer)

        async def add_sqlite(table, img_name, path_name, character, title, hair, tags, ero):
            print(f"{img_name}")
            # user_obj = table(img_name=img_name, character=character, work_name=work_name,tags=tags,ero=ero)
            # orm.add(table, user_obj)
            await engine.insert_or_update(table, ([ImageInformation.img_name == f"{img_name}"]),
                                          {"img_name": img_name,
                                           "path_name": path_name,
                                           "character": character,
                                           "title": title,
                                           "hair": hair,
                                           "tags": tags,
                                           "ero": ero})

        for file in os.listdir(self.FileDirName.get()):
            await add_sqlite(ImageInformation, file, "ero", "none", "none", "none", "none", 5)

    async def gui_in(self, app_loop):
        # ero_in_frame 将图片导入数据库
        ero_in_frame = tk.Frame(self)
        ero_in_frame.pack(side="left")

        tk.Label(ero_in_frame, text="初始化").grid(row=2, column=0)
        tk.Label(ero_in_frame, text="数据库名称：").grid(row=0, column=0)
        tk.Entry(ero_in_frame, textvariable=self.db_name, state=tk.DISABLED, width=30).grid(row=0, column=1)
        # tk.Button(ero_in_frame, text="选择数据库").grid(row=0, column=2)

        tk.Label(ero_in_frame, text="图片所在目录：").grid(row=1, column=0)
        tk.Entry(ero_in_frame, textvariable=self.FileDirName, state=tk.DISABLED, width=30).grid(row=1, column=1)
        # tk.Button(ero_in_frame, text="选择图片目录").grid(row=1, column=2)

        tk.Button(ero_in_frame, text="开始导入", command=lambda: app_loop.create_task(self.Batch_write())).grid(row=2,
                                                                                                            column=1)

    async def gui_out(self, app_loop):
        ero_out_frame = tk.Frame(self)
        ero_out_frame.pack(side="left")

        # ero_out_frame 显示所选图片信息
        tk.Label(ero_out_frame, text="显示并修改图片信息").grid(row=0, column=1)
        tk.Label(ero_out_frame, text="图片文件名：").grid(row=1, column=0)
        tk.Entry(ero_out_frame, textvariable=self.ero_img_name, state=tk.DISABLED).grid(row=1, column=1)
        tk.Label(ero_out_frame, text="图片所在文件夹：").grid(row=2, column=0)
        tk.Entry(ero_out_frame, textvariable=self.ero_path_name, state=tk.DISABLED).grid(row=2, column=1)
        tk.Label(ero_out_frame, text="图片中的角色：").grid(row=3, column=0)
        tk.Entry(ero_out_frame, textvariable=self.ero_character).grid(row=3, column=1)
        tk.Label(ero_out_frame, text="角色来源作品名：").grid(row=4, column=0)
        tk.Entry(ero_out_frame, textvariable=self.ero_title).grid(row=4, column=1)
        tk.Label(ero_out_frame, text="角色头发：").grid(row=5, column=0)
        tk.Entry(ero_out_frame, textvariable=self.ero_hair).grid(row=5, column=1)
        tk.Label(ero_out_frame, text="其他图片标签：").grid(row=6, column=0)
        tk.Entry(ero_out_frame, textvariable=self.ero_tags).grid(row=6, column=1)
        tk.Label(ero_out_frame, text="主观ero度：").grid(row=7, column=0)
        tk.Entry(ero_out_frame, textvariable=self.ero_ero).grid(row=7, column=1)
        tk.Label(ero_out_frame, text="选择图片：").grid(row=8, column=0)
        combo = ttk.Combobox(ero_out_frame, values=self.ero_list, width=17)
        combo.grid(row=8, column=1)
        tk.Button(ero_out_frame, text="打开图片", command=lambda: app_loop.create_task(self.get_list())).grid(row=8, column=2)
        tk.Button(ero_out_frame, text="上一张", width=10).grid(row=9, column=0)
        tk.Button(ero_out_frame, text="下一张", width=10).grid(row=9, column=1)
        tk.Button(ero_out_frame, text="确认修改").grid(row=10, column=1)

    async def gui_show(self, app_loop):
        # ero_show_frame 显示所选图片
        ero_show_frame = tk.Frame(self)
        ero_show_frame.pack(side="right")
        tk.Label(ero_show_frame, text="显示所选图片").grid(row=0, column=1)
        # global img_png
        # img_png = r"D:\automata-toolbox\test_img\00101.jpg"
        # img_open = Image.open(self.img_png).resize((480, 268))
        # img_open_pil = ImageTk.PhotoImage(img_open)
        ero_show = tk.Label(ero_show_frame, image=self.img_open_pil)
        ero_show.grid(row=1, column=1)

    async def get_list(self):
        pass

    async def updater(self, interval):
        while True:
            self.update()
            await asyncio.sleep(interval)

    def close(self):
        for task in self.tasks:
            task.cancel()
        self.loop.stop()
        self.destroy()


loop = asyncio.get_event_loop()
app = App(loop)
loop.run_forever()
loop.close()
loop.stop()
