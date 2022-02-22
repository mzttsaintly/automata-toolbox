import asyncio
import os
import tkinter as tk
from tkinter import ttk
from typing import List, Tuple

from PIL import Image, ImageTk
from loguru import logger

from EroLibrary.erolibrary import AsyncEngine, AsyncORM
from sqlalchemy import Column, Integer, String, func
from sqlalchemy.sql.expression import select, and_
from sqlalchemy.ext.declarative import declarative_base

print("输入数据库名字（非根目录下需输入完整路径）")
sqlite_host = input()
print("输入图片文件夹路径（绝对路径）")
img_path = input()
# print(f"数据库：{sqlite_host}\n文件夹：{img_path}")
logger.success(f"数据库：{sqlite_host}\n文件夹：{img_path}")
engine = AsyncORM(f"sqlite+aiosqlite:///{sqlite_host}")
Base = engine.Base


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


async def get_info(where) -> List[Tuple[int, str, str, str, str, str, str, int]]:
    """
    where: 需要检索的条件，填写关系式，如(Setu.time > f"{datetime.date.now()}")
                     若需要填写多个关系式请用and_()连接；如and_(Setu.time > f"{datetime.date.today()}",
                                                       Setu.Group_id == f"{group_id}")
    返回符合条件的条目信息。
    :return: list[tuple(id: int,img_name: str,path_name: str,character: str ,title: str ,hair: str,tags: str,
    ero: int)]
    """
    await engine.create_all()
    res = await engine.search_sqlite_in_table_by_where((ImageInformation.id, ImageInformation.img_name,
                                                        ImageInformation.path_name, ImageInformation.character,
                                                        ImageInformation.title, ImageInformation.hair,
                                                        ImageInformation.tags, ImageInformation.ero), where)
    return res


class App(tk.Tk):

    def __init__(self, app_loop, interval=1 / 60):
        super(App, self).__init__()
        self.dir = None
        self.loop = app_loop
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.title('EroLibrary')
        self.geometry('1080x500')
        self.ero_id = 0
        self.ero_img_name = tk.StringVar()
        self.ero_path_name = tk.StringVar()
        self.ero_character = tk.StringVar()
        self.ero_character_list = []
        self.ero_title = tk.StringVar()
        self.ero_title_list = []
        self.ero_hair = tk.StringVar()
        self.ero_hair_list = []
        self.ero_tags = tk.StringVar()
        self.ero_tags_list = []
        self.ero_ero = tk.IntVar()
        self.ero_ero_list = []
        self.ero_list = ["None"]
        self.max = 99999

        self.db_name = tk.StringVar()
        self.FileDirName = tk.StringVar()
        
        self.img_png = f"{os.path.join(os.getcwd(), 'res', os.listdir(os.path.join(os.getcwd(), 'res'))[0])}"
        self.img_open = Image.open(self.img_png).resize((480, 268))
        self.img_open_pil = ImageTk.PhotoImage(self.img_open)
        self.tasks = []
        self.tasks.append(app_loop.create_task(self.sqlite_link()))
        self.tasks.append(app_loop.create_task(self.gui_in(app_loop)))
        self.tasks.append(app_loop.create_task(self.gui_out(app_loop)))
        self.tasks.append(app_loop.create_task(self.gui_show(app_loop)))
        self.tasks.append(app_loop.create_task(self.updater(interval)))

    async def sqlite_link(self):
        await engine.create_all()
        self.db_name.set(f"{sqlite_host}")
        self.FileDirName.set(f"{img_path}")
        self.dir = self.FileDirName.get().split("\\")[-1]
        logger.debug(f"dir = {self.dir}")
        # Base = engine.Base
        # await engine.create_all()
        # self.img_png = f"{self.FileDirName.get() + os.sep + os.listdir(self.FileDirName.get())[0]}"
        # print(f"{self.img_png}")

    async def Batch_write(self):
        await engine.create_all()

        async def add_sqlite(table, img_name, path_name, character, title, hair, tags, ero):
            # print(f"{img_name}")
            logger.success(f"{img_name}")
            # user_obj = table(img_name=img_name, character=character, work_name=work_name,tags=tags,ero=ero)
            # orm.add(table, user_obj)
            await engine.insert_or_ignore(table, ([ImageInformation.img_name == f"{img_name}"]),
                                          {"img_name": img_name,
                                           "path_name": path_name,
                                           "character": character,
                                           "title": title,
                                           "hair": hair,
                                           "tags": tags,
                                           "ero": ero})

        for file in os.listdir(self.FileDirName.get()):
            await add_sqlite(ImageInformation, file, self.dir, "Unknown", "Unknown", "Unknown", "Unknown", 5)

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

        tk.Button(ero_in_frame, text="导入数据库", command=lambda: app_loop.create_task(self.Batch_write())).grid(row=2,
                                                                                                             column=1)
        tk.Button(ero_in_frame, text="读取数据库信息", command=lambda: app_loop.create_task(self.get_ero_name_list())) \
            .grid(row=3,
                  column=1)

    async def gui_out(self, app_loop):
        ero_out_frame = tk.Frame(self)
        ero_out_frame.pack(side="left")

        # ero_out_frame 显示所选图片信息
        tk.Label(ero_out_frame, text="显示并修改图片信息").grid(row=0, column=1)
        tk.Label(ero_out_frame, text="图片文件名：").grid(row=1, column=0)
        global ero_out_name, ero_out_path, ero_out_character, ero_out_title, ero_out_hair, ero_out_tags, ero_out_ero
        ero_out_name = tk.Entry(ero_out_frame, textvariable=self.ero_img_name, state=tk.DISABLED)
        ero_out_name.grid(row=1, column=1)
        tk.Label(ero_out_frame, text="图片所在文件夹：").grid(row=2, column=0)
        ero_out_path = tk.Entry(ero_out_frame, textvariable=self.ero_path_name, state=tk.DISABLED)
        ero_out_path.grid(row=2, column=1)
        tk.Label(ero_out_frame, text="图片中的角色：").grid(row=3, column=0)
        ero_out_character = ttk.Combobox(ero_out_frame, textvariable=self.ero_character, values=self.ero_character_list)
        ero_out_character.grid(row=3, column=1)
        tk.Label(ero_out_frame, text="角色来源作品名：").grid(row=4, column=0)
        ero_out_title = ttk.Combobox(ero_out_frame, textvariable=self.ero_title, values=self.ero_title_list)
        ero_out_title.grid(row=4, column=1)
        tk.Label(ero_out_frame, text="角色头发：").grid(row=5, column=0)
        ero_out_hair = ttk.Combobox(ero_out_frame, textvariable=self.ero_hair, values=self.ero_hair_list)
        ero_out_hair.grid(row=5, column=1)
        tk.Label(ero_out_frame, text="其他图片标签：").grid(row=6, column=0)
        ero_out_tags = ttk.Combobox(ero_out_frame, textvariable=self.ero_tags, values=self.ero_tags_list)
        ero_out_tags.grid(row=6, column=1)
        tk.Label(ero_out_frame, text="主观ero度：").grid(row=7, column=0)
        ero_out_ero = ttk.Combobox(ero_out_frame, textvariable=self.ero_ero, values=self.ero_ero_list)
        ero_out_ero.grid(row=7, column=1)
        tk.Label(ero_out_frame, text="选择图片：").grid(row=8, column=0)
        global combo
        combo = ttk.Combobox(ero_out_frame, values=self.ero_list, width=17)
        combo.grid(row=8, column=1)
        tk.Button(ero_out_frame, text="确认选择", command=lambda: app_loop.create_task(self.choose_combo())) \
            .grid(row=8, column=2)
        tk.Button(ero_out_frame, text="上一张", command=lambda: app_loop.create_task(self.before_ero()), width=10) \
            .grid(row=9, column=0)
        tk.Button(ero_out_frame, text="下一张", command=lambda: app_loop.create_task(self.next_ero()), width=10) \
            .grid(row=9, column=1)
        tk.Button(ero_out_frame, text="写入修改", command=lambda: app_loop.create_task(self.update_sql()))\
            .grid(row=10, column=1)

    async def gui_show(self, app_loop):
        # ero_show_frame 显示所选图片
        ero_show_frame = tk.Frame(self)
        ero_show_frame.pack(side="left")
        tk.Label(ero_show_frame, text="显示所选图片").grid(row=0, column=1)
        global ero_show
        ero_show = tk.Label(ero_show_frame, image=self.img_open_pil)
        # print(f"{self.img_png}")
        logger.success(f"当前图片：{self.img_png}")
        ero_show.grid(row=1, column=1)

    async def update_info(self, res):
        # print(f"{self.img_png}")
        # 刷新信息
        self.ero_id = res[0][0]
        self.ero_img_name.set(res[0][1])
        self.ero_path_name.set(res[0][2])
        self.ero_character.set(res[0][3])
        self.ero_title.set(res[0][4])
        self.ero_hair.set(res[0][5])
        self.ero_tags.set(res[0][6])
        self.ero_ero.set(res[0][7])
        ero_out_name.config(textvariable=self.ero_img_name)
        ero_out_path.config(textvariable=self.ero_path_name)
        ero_out_character.config(textvariable=self.ero_character)
        ero_out_title.config(textvariable=self.ero_title)
        ero_out_hair.config(textvariable=self.ero_hair)
        ero_out_tags.config(textvariable=self.ero_tags)
        ero_out_ero.config(textvariable=self.ero_ero)
        # 刷新图片
        self.img_png = f"{os.path.join(self.FileDirName.get(), self.ero_img_name.get())}"
        logger.success(f"当前图片：{self.img_png}")
        self.img_open = Image.open(self.img_png)
        width, height = self.img_open.size
        self.img_open = self.img_open.resize((int(width / 4), int(height / 4)))
        self.img_open_pil = ImageTk.PhotoImage(self.img_open)
        ero_show.config(image=self.img_open_pil)
        ero_show.image = self.img_open_pil
        self.update_idletasks()  # 更新后必须update

    async def get_ero_name_list(self):
        res = await get_info(ImageInformation.id > 0)
        self.max = (await engine.query_one(func.max(ImageInformation.id)))[0]
        logger.debug(f"id最大值为{self.max}")
        self.ero_character_list = await engine.select_distinct(ImageInformation.character)
        self.ero_title_list = await engine.select_distinct(ImageInformation.title)
        self.ero_hair_list = await engine.select_distinct(ImageInformation.hair)
        self.ero_tags_list = await engine.select_distinct(ImageInformation.tags)
        self.ero_ero_list = await engine.select_distinct(ImageInformation.ero)
        ero_out_character.config(values=self.ero_character_list)
        ero_out_title.config(values=self.ero_title_list)
        ero_out_hair.config(values=self.ero_hair_list)
        ero_out_tags.config(values=self.ero_hair_list)
        ero_out_ero.config(values=self.ero_ero_list)

        ans = []
        for i in range(len(res)):
            ans.append(res[i][1])
        self.ero_list = ans
        combo.config(values=self.ero_list)
        combo.values = self.ero_list
        logger.success(f"从{self.db_name.get()}中读取到数据")
        self.update_idletasks()

    async def update_sql(self):
        name = ero_out_name.get()
        character = ero_out_character.get()
        title = ero_out_title.get()
        hair = ero_out_hair.get()
        tags = ero_out_tags.get()
        ero = ero_out_ero.get()
        await engine.update(ImageInformation, ([ImageInformation.id == self.ero_id,
                                                ImageInformation.img_name == f"{name}"]),
                            {"character": character,
                             "title": title,
                             "hair": hair,
                             "tags": tags,
                             "ero": ero})
        logger.success(f"成功写入信息\n‘‘character’: {character},\n‘title’: {title},\n‘hair’: {hair},"
                       f"‘tags’: {tags},\n "
                       f"‘ero’: {ero}")
    # "img_name": name

    async def choose_combo(self):
        self.ero_img_name.set(combo.get())
        res = await get_info(ImageInformation.img_name == self.ero_img_name.get())
        await self.update_info(res)

    async def next_ero(self):
        if self.ero_id < self.max:
            self.ero_id += 1
            res = await get_info(ImageInformation.id == self.ero_id)
            await self.update_info(res)
        else:
            logger.debug(f"下面没有了哟")

    async def before_ero(self):
        if self.ero_id > 1:
            self.ero_id -= 1
            res = await get_info(ImageInformation.id == self.ero_id)
            await self.update_info(res)
        else:
            logger.debug(f"已经到头了哟")

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
