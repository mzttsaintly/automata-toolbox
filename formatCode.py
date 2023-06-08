import re
import os
import loguru

log = loguru.logger

link_pattern = re.compile('src="(.*?)"')

def get_src(file):
    with open(file, 'r', encoding='utf-8') as f:
        res = f.read()
        res_list = re.findall(link_pattern, res)
        return res_list


def make_obj(res_list):
    new_res = []
    for i in range(len(res_list)):
        new_res.append(f'const img{str(i).rjust(3,"0")} = {res_list[i]}')
    log.debug(new_res)


def get_dir(path_name):
    os.chdir(path_name)
    print(path_name)
    for file in os.listdir(path_name):
        log.debug(file)
        if os.path.splitext(file)[-1] == ".vue":
            make_obj(get_src(file))


if __name__ == "__main__":
    # make_obj(get_src(f'./vue/2start.vue'))
    get_dir("Z:/automata-toolbox/vue")
