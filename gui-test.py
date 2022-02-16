import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.filedialog import askdirectory
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BLOB
from sqlalchemy import update, insert, delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import select, and_
import asyncio
import os


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

# sqlite_host = r"warfarin.db"
# img_path = r"/test_img"
Base = None


class AsyncEngine:
    def __init__(self, db_link):
        self.engine = create_async_engine(
            db_link,
            echo=False
        )

    async def execute(self, sql, **kwargs):
        async with AsyncSession(self.engine) as session:
            try:
                result = await session.execute(sql, **kwargs)
                await session.commit()
                return result
            except Exception as e:
                await session.rollback()
                raise e

    async def fetchall(self, sql):
        return (await self.execute(sql)).fetchall()

    async def fetchone(self, sql):
        # self.warning(sql)
        result = await self.execute(sql)
        one = result.fetchone()
        if one:
            return one
        else:
            return None

    async def fetchone_dt(self, sql, n=999999):
        # self.warning(sql)
        result = await self.execute(sql)
        columns = result.keys()
        length = len(columns)
        for _ in range(n):
            one = result.fetchone()
            if one:
                yield {columns[i]: one[i] for i in range(length)}


class AsyncORM(AsyncEngine):
    def __init__(self, conn):
        super().__init__(conn)
        print(f"{conn}")
        self.session = AsyncSession(bind=self.engine)
        self.Base = declarative_base(self.engine)
        self.async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def create_all(self):
        """创建所有表"""
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)
        print("创建连接")

    async def drop_all(self):
        """删除所有表"""
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.drop_all)

    async def add(self, table, dt):
        """添加信息"""
        async with self.async_session() as session:
            async with session.begin():
                session.add(table(**dt), _warn=False)
            await session.commit()

    async def update(self, table, condition, dt):
        """更新信息"""
        await self.execute(update(table).where(*condition).values(**dt))

    async def load_all(self, sql):
        """查询信息
        sql: 查询指令
        例： engine.load_all(select(Setu.user_id, Setu.time).where(Setu.time > f"{datetime.date.today()}"))"""
        return (await self.execute(sql)).fetchall()

    async def insert_or_update(self, table, condition, dt):
        if (await self.execute(select(table).where(*condition))).all():
            return await self.execute(update(table).where(*condition).values(**dt))
        else:
            return await self.execute(insert(table).values(**dt))

    async def insert_or_ignore(self, table, condition, dt):
        if not (await self.execute(select(table).where(*condition))).all():
            return await self.execute(insert(table).values(**dt))

    async def delete(self, table, condition):
        return await self.execute(delete(table).where(*condition))

    async def init_check(self) -> bool:
        for table in Base.__subclasses__():
            try:
                await self.fetchone(select(table))
            except OperationalError:
                async with self.engine.begin() as conn:
                    await conn.run_sync(table.__table__.create(self.engine))
                return False
        return True


if __name__ == "__main__":
    print("输入数据库名字（非根目录下需输入完整路径）")
    sqlite_host = input()
    print("输入图片文件夹路径（绝对路径）")
    img_path = input()
    print(f"数据库：{sqlite_host}\n文件夹：{img_path}")

    engine = AsyncORM(f"sqlite+aiosqlite:///{sqlite_host}")
    Base = engine.Base


class ImageInformation(Base):
    __tablename__ = "image_information"
    id = Column(Integer, primary_key=True, autoincrement=True)
    img_name = Column(String(32))
    path_name = Column(String(32))
    character = Column(String(32))
    title = Column(String(32))
    hair = Column(String(32))
    tags = Column(String(32))
    ero = Column(Integer)


async def Batch_write():
    await engine.create_all()

    async def add_sqlite(table, img_name, path_name, character, title, hair, tags, ero):
        print(f"{img_name}")
        # user_obj = table(img_name=img_name, character=character, work_name=work_name,tags=tags,ero=ero)
        # orm.add(table, user_obj)
        await engine.add(table,
                         {"img_name": img_name,
                          "path_name": path_name,
                          "character": character,
                          "title": title,
                          "hair": hair,
                          "tags": tags,
                          "ero": ero})

    for file in os.listdir(img_path):
        await add_sqlite(ImageInformation, file, "ero", "none", "none", "none", "none", 5)


async def search_sqlite_in_table_by_where(table_and_column, search_equation):
    """
    从表中搜索符合条件的数据
    table_and_column: 表名和表内的项目名，可填多个(Setu.Group_id, Setu.user_id, Setu.time etc.)
    search_equation: 搜索的条件,填写关系式，如(Setu.time > f"{datetime.date.now()}")
                     若需要填写多个关系式请用and_()连接；如and_(Setu.time > f"{datetime.date.today()}",
                                                       Setu.Group_id == f"{group_id}")
    """
    # today = datetime.date.today()
    # tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    res = await engine.load_all(select(table_and_column).where(search_equation))
    return res


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(Batch_write())
