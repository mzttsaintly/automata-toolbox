import re
import os
import loguru

log = loguru.logger

def get_src(file):
    with open(file, 'r', encoding='utf-8') as f:
        res = f.read()
        res_list = re.findall()