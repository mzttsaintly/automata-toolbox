from sqlalchemy import Column, Integer, String, DateTime, Boolean, BLOB
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import asyncio
import os

print("输入数据库名字（非根目录下需输入完整路径）")
msg = input()
print("输入图片文件夹路径（绝对路径）")
msg2 = input()
print(f"数据库：{msg}\n文件夹：{msg2}")
sqlite_host = r"warfarin.db"
img_path = r"D:/automata-toolbox/test_img"


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

    async def load_all(self, sql):
        """查询信息
        sql: 查询指令
        例： engine.load_all(select(Setu.user_id, Setu.time).where(Setu.time > f"{datetime.date.today()}"))"""
        return (await self.execute(sql)).fetchall()


engine = AsyncORM(f"sqlite+aiosqlite:///{sqlite_host}")
Base = engine.Base


class ImageInformation(Base):
    __tablename__ = "image_information"
    id = Column(Integer, primary_key=True, autoincrement=True)
    img_name = Column(String(32))
    character = Column(String(32))
    work_name = Column(String(32))
    tags = Column(String(32))
    ero = Column(Integer)


async def Batch_write():
    await engine.create_all()

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

    for file in os.listdir(img_path):
        await add_sqlite(ImageInformation, file, "none", "none", "none", 0)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(Batch_write())
