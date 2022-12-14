#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
定时从网络上备份github的dns,并写到系统host中
"""

import logging
import os
import platform
import datetime
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

host_window = r"C:\Windows\System32\drivers\etc\hosts"
host_unix = r"/etc/hosts"
api_host = "https://gitlab.com/ineo6/hosts/-/raw/master/next-hosts"


def get_http_content():
    """查询dns github最佳解析路线"""
    # noinspection HttpUrlsUsage
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36',
    }
    res = requests.get(api_host, headers=headers, timeout=5)
    return res.text


def read_local(filename="hosts.txt"):
    """取当前目录的指定文件内容"""
    path = os.path.dirname(__file__) + "/"
    with open(path + filename, 'r', encoding='utf-8') as f:
        return f.read()


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


def set_host():
    """设置host文件"""
    time = datetime.datetime.now()
    # 从http中读取内容
    text = get_http_content()
    if not text:
        logger.warning('读取http内容为空~')
        return
    # 从本地读取文件内容
    local = read_local('hosts.txt')
    # 合并内容
    host_text = '\n'.join(['# 更新时间:' + str(time) + '\n', local, text])
    # print(host_text)
    # return
    # 写入到系统host中
    write_host(host_text)
    if platform.system() == 'Windows':
        os.system('ipconfig /flushdns')
    # 写入日志
    logger.info('设置成功， 时间:{} '.format(time))


if __name__ == '__main__':
    set_host()
