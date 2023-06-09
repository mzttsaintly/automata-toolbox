import re
import os
import loguru

log = loguru.logger

link_pattern = re.compile('src="(.*?)"')


def get_src(file):
    with open(file, 'r+', encoding='utf-8') as f:
        res = f.read()
        res_list = re.findall(link_pattern, res)
        new_res = make_obj(res_list)
        content_add = "\r".join(new_res)
        # log.debug(content_add)
        pos = res.find('<script>')
        log.debug('pos is:' + str(pos))
    with open(file, 'w', encoding='utf-8') as f:
        if pos != -1:
            res = res[:pos+8] + content_add + res[pos+8:]
            f.write(res)


def make_obj(res_list):
    new_res = []
    for i in range(len(res_list)):
        new_res.append(f'const img{str(i).rjust(3, "0")} = {res_list[i]}')
    log.debug(new_res)
    return new_res


def get_dir(path_name):
    os.chdir(path_name)
    print(path_name)
    for file in os.listdir(path_name):
        log.debug(file)
        if os.path.splitext(file)[-1] == ".vue":
            get_src(file)


if __name__ == "__main__":
    # get_src(f'D:\\wy\\automata-toolbox\\vue\\2start.vue')
    get_dir("D:\\wy\\automata-toolbox\\vue")
