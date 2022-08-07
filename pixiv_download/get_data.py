import random
from base64 import b64encode
from pathlib import Path
from PIL import Image
from io import BytesIO


# 随机修改左上角第一颗像素的颜色,并且返还图片的base64编码
async def change_pixel(image, quality):
    image = image.convert("RGB")
    image.load()[0, 0] = (random.randint(0, 255),
                          random.randint(0, 255), random.randint(0, 255))
    byte_data = BytesIO()
    image.save(byte_data, format="JPEG", quality=quality)
    # pic是的图片的base64编码
    pro_pic = b64encode(byte_data.getvalue()).decode()
    return pro_pic
