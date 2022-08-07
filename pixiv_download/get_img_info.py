import httpx


def get_img_info(img_id: int, only_proxy: bool = True):
    hibiapi_url = "https://api.obfs.dev/api/pixiv/illust"
    params = {'id': img_id}
    res = httpx.get(url=hibiapi_url, params=params)
    if res.status_code == 200:
        print("成功获取图片信息")
        if only_proxy:  # 只需要返回图片链接
            img_info = res.json()
            if img_info['illust']['meta_single_page']:  # 区分单张和多张
                img_url = str(img_info['illust']['meta_single_page']['original_image_url'])
                proxy_url = img_url.replace('i.pximg.net', 'i.pixiv.re')
            else:
                proxy_url = []
                url_list = img_info['illust']['meta_pages']
                for item in url_list:
                    img_url = str(item['image_urls']['original'])
                    single_proxy_url = img_url.replace('i.pximg.net', 'i.pixiv.re')
                    proxy_url.append(single_proxy_url)
            return proxy_url

        else:  # 返回包括图片链接的各种信息
            img_info = res.json()
            if img_info['illust']['meta_single_page']:  # 区分单张和多张
                img_url = str(img_info['illust']['meta_single_page']['original_image_url'])
                proxy_url = img_url.replace('i.pximg.net', 'i.pixiv.re')
            else:
                img_url = str(img_info['illust']['meta_pages'][0]['image_urls']['original'])
                proxy_url = img_url.replace('i.pximg.net', 'i.pixiv.re')
            print(f"id = {img_info['illust']['id']}")
            print(f"title = {img_info['illust']['title']}")
            print(f"original_image_url = {img_url}")
            print(f"proxy_url = {proxy_url}")
            return img_info

    else:
        print(f"出现错误，错误代码：{res.status_code}")


if __name__ == "__main__":
    while True:
        print("请输入作品id：(按Ctrl + C 退出）")
        img_id = int(input())
        print(get_img_info(img_id))
