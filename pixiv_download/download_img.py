import httpx
from PIL import Image
from io import BytesIO


# from .get_img_info import get_img_info


def download_img(img_url: str, save_path: str):
    res = httpx.get(img_url, timeout=10)
    image = Image.open(BytesIO(res.read()))
    image.save(save_path)


if __name__ == "__main__":
    na = "https://i.pixiv.re/img-original/img/2019/09/15/00/09/07/76783762_p0.jpg"
    ext_name = na.split('/')[-1]
    download_img(na, f"{ext_name}")
