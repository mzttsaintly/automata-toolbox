import asyncio
import os
from SqliteInImg.sqlite_link import *
from SqliteInImg.table import *


img_path = r"D:/automata-toolbox/test_img"

# engine = AsyncORM(f"sqlite+aiosqlite:///{sqlite_host}")
# Base = engine.Base


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
