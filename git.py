#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
定时从网络上备份github的dns,并写到系统host中
"""

import logging
import os
import platform
import datetime
import re
import json
import getip

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

host_window = r"C:\Windows\System32\drivers\etc\hosts"
host_unix = r"/etc/hosts"


def _get_path():
    """获取host路径"""
    if platform.system() == "Windows":
        return host_window
    return host_unix


def read_host():
    """读取host"""
    with open(_get_path(), 'r', encoding='utf-8') as f:
        return f.read()


def write_host(text):
    """写入host"""
    with open(_get_path(), 'w+', encoding='utf-8') as f:
        return f.write(text)


def github_host():
    """爬虫获取的host"""
    with open('conf.json', encoding="utf-8") as json_file:
        json_obj = json.load(json_file)
    return json_obj


def set_host():
    """设置host文件"""
    time = datetime.datetime.now()
    # 从http中读取内容
    json_obj = github_host()
    hosts = ''
    for domain in json_obj['sites']:
        ip = getip.Getip.get(domain)
        hosts += f"{ip:<30}{domain} \n"
    # print(hosts)
    # 从本地读取文件内容
    local = read_host()
    local = re.sub(r'# ==== GitHub Host Start ====([.|\S|\s]*)# ==== GitHub Host End ====', '', local, 0, re.M)
    # print(ret)
    # 合并内容
    host_text = '\n'.join([
        local,
        '# ==== GitHub Host Start ====',
        '# Update at: '+str(time),
        hosts,
        '# ==== GitHub Host End ===='
    ])
    # 写入到系统host中,并刷新dns
    write_host(host_text)
    if platform.system() == 'Windows':
        os.system('ipconfig /flushdns')
    # 写入日志
    logger.info('设置成功， 时间:{} '.format(time))


if __name__ == '__main__':
    set_host()
