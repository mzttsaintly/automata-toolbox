from EroLibrary.erolibrary import *
from EroLibrary.erolibrary import AsyncEngine, AsyncORM
from sqlalchemy import Column, Integer, String, func
from loguru import logger
import asyncio

print("输入数据库名字（非根目录下需输入完整路径）")
sqlite_host = input()
# print("输入图片文件夹路径（绝对路径）")
# img_path = input()
# # print(f"数据库：{sqlite_host}\n文件夹：{img_path}")
# logger.success(f"数据库：{sqlite_host}\n文件夹：{img_path}")
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


async def d(condition):
    res = await engine.select_distinct(condition)
    logger.success(f"内容为：{res}")


async def count(table):
    # res = await engine.query_one(func.count(table))
    res = await engine.query_count(table)
    logger.success(f"count 内容为{res}")


async def max_num(table):
    res = (await engine.query_one(func.max(table)))
    logger.success(f"max_num = {res}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(d(ImageInformation.character))
    loop.run_until_complete(d(ImageInformation.ero))
    loop.run_until_complete(d(ImageInformation.hair))
    loop.run_until_complete(d(ImageInformation.tags))
    loop.run_until_complete(count(ImageInformation.character))
    loop.run_until_complete(count(ImageInformation.ero))
    loop.run_until_complete(count(ImageInformation.hair))
    loop.run_until_complete(max_num(ImageInformation.character))
    loop.run_until_complete(max_num(ImageInformation.ero))
    loop.run_until_complete(max_num(ImageInformation.hair))
