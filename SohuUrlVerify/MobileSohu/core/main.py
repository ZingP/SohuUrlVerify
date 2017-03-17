#! /usr/bin/env python3
import requests
import logging
from bs4 import BeautifulSoup
from core.pool import ThreadPool
from conf import settings

# 设置日志格式
logging.basicConfig(filename=settings.ERROR_LOG,
                    format='%(asctime)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=40)


def url_filter(a_tags):
    """
    将所有的a标签进行处理。
    :param a_tags: a标签列表（迭代队象）
    :return: li: url列表
    """
    li = []
    for link in a_tags:
        href = link.get('href', None)
        if href:
            if href.startswith('http'):
                url = href
            elif href.startswith('#') or href.startswith('javascript') or href.startswith('//'):
                pass
            else:
                url = settings.BASE_URL[:-1] + href
            if url.startswith(settings.BASE_URL) and url != settings.BASE_URL:
                li.append(url)
    return li


def verify(url, p):
    """
    验证url可达性和递归。
    :param url： url字符串；
    :param p： 线程池对象；
    :return: None
    """
    ret = requests.get(url=url)
    if ret.status_code == 200:
        soup = BeautifulSoup(ret.text, 'lxml')
        url_list = url_filter(soup.find_all('a'))
        for url in url_list:
            p.run(verify, (url, p,), callback=callback(p))
    else:
        print("no>>:%s" % url)
        msg = "%s-%s" % (url,ret.status_code)
        logging.error(msg)


def callback(p):
    """
    线程池的回调函数。当线程池中的线程小于设定的线程数，打印一下线程数量。
    测试用。
    """
    if len(p.generate_list) < p.max_num:
        print(len(p.generate_list))


def main():
    """主函数"""
    p = ThreadPool(settings.THREAD_NUM)
    p.run(verify, (settings.BASE_URL, p,), callback=callback(p,))



