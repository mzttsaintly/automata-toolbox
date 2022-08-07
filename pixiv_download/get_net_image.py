import aiohttp
from PIL import Image
from io import BytesIO
from .get_data import change_pixel


async def lolicon(key="", r18=False, num=1, quality=75):
    data_list = await get_net_image(key, r18, num)
    pic_list = []
    for data in data_list:
        pic_list.append(await deal_net_image(data, quality))
    return pic_list


async def get_net_image(key="", r18=False, num=1):
    """
    从api中获取图片
    Args:
        key: 图片关键词
        r18: 是否r18
        num: 图片数量

    Returns:图片信息列表

    """
    # url = f"https://api.lolicon.app/setu/v2?r18={1 if r18 else 0}&tag={key}&num={num}"

    url = "https://api.lolicon.app/setu/v2"
    r18_flag = 1 if r18 else 0
    key_list = key.split()
    params = {'tag': key_list, 'r18': r18_flag, 'num': num}
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as resp:
            result = await resp.json()
    return result["data"]


async def deal_net_image(data, quality):
    """
    处理网页返回的信息
    Args:
        quality: 图片质量
        data: 图片信息列表

    Returns:
        list: [图片base64，图片信息，True/False]

    """
    try:
        pid = data["pid"]
        setu_title = data["title"]
        setu_author = data["author"]
        setu_tag = data["tags"]
        setu_url = data["urls"]["original"].replace('i.pixiv.cat', 'i.pixiv.re')
        # logger.info(f"标题：{setu_title}，作者：{setu_author}，tag：{setu_tag}，pid：{pid}，url：{setu_url}")
        # 下载图片并转换左上角第一个像素
        img = await change_pixel(await down_img(setu_url), quality)
        plain = f"标题：{setu_title}，\n画师：{setu_author}，\ntag：{setu_tag}，\npid:{pid}"
        # 返回一个由图片base64序列，图片信息，True/False 组成的列表
        return [img, plain, True]
    except AttributeError:
        return [None, "error:api未找到图片", False]


async def down_img(url):
    """
    根据链接下载图片
    Args:
        url: 图片链接

    Returns: 图片bytes数据或错误代码

    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as resp:
            if resp.status == 200:
                image = Image.open(BytesIO(await resp.read()))
                return image
            else:
                raise
