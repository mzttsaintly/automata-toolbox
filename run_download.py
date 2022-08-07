import os
from pixiv_download.get_img_info import get_img_info
from pixiv_download.download_img import download_img


save_div_path = "./res"

while True:
    print("请输入作品id：(按Ctrl + C 退出）")
    img_id = int(input())
    img_info = get_img_info(img_id)
    if isinstance(img_info, list):
        for img_url in img_info:
            save_path = save_div_path + os.path.sep + img_url.split('/')[-1]
            download_img(img_url, save_path)
    else:
        save_path = save_div_path + os.path.sep + img_info.split('/')[-1]
        download_img(img_info, save_path)
