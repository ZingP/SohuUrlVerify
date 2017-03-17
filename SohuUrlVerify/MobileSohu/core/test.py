#! /usr/bin/env python3
"""
测试模块，本模块用于测试多进程+加协程模式来实现需求。
"""
"""
题目：
请设计一个系统，自动完成对于手机搜狐(http://m.sohu.com/)系统可靠性的检测。具体要求：
1. 递归检测所有m.sohu.com域名的页面以及这些页面上的链接的可达性，即有没有出现不可访问情况。
2. m.sohu.com域名页面很多，从各个方面考虑性能优化。
3. 对于错误的链接记录到日志中，日志包括：URL，时间，错误状态等。
要求：不使用框架。 加分项：使用并发方式实现。
"""
from bs4 import BeautifulSoup
import requests
from multiprocessing import Process
import gevent
from gevent import monkey
monkey.patch_all()


def url_filter(a_list):
    """
    将所有的a标签进行处理。
    :param a_list: a标签列表（迭代队象）
    :return: li: url列表
    """
    li = []
    for link in a_list:
        href = link.get('href', None)
        if href:
            if href.startswith('http'):
                url_ = href
            elif href.startswith('#') or href.startswith('javascript') or href.startswith('//'):
                pass
            else:
                url_ = 'http://m.sohu.com' + href
            if url_.startswith('http://m.sohu.com/') and url_ != 'http://m.sohu.com/':
                li.append(url_)
    return li


def process_start(url_list):
    """
    使用协程。
    :param url_list: url列表（迭代队象）
    :return: None
    """
    li = []
    for _ in url_list:
        li.append(gevent.spawn(verify, _))
    gevent.joinall(li)


# 存放递归获取来的URL，当作栈使用
tasks = []


def verify(url):
    """
    验证url可达性和递归。
    :param url： url字符串。
    :return: None
    """
    try:
        ret = requests.get(url=url)
    except Exception as e:
        print(e)
    else:
        if ret.status_code == 200:
            soup = BeautifulSoup(ret.text, 'lxml')
            url_list = url_filter(soup.find_all('a'))
            if url_list:
                for url in url_list:
                    if len(tasks) >= 100:
                        tasks_list = []
                        for i in range(len(tasks)):
                            tasks_list.append(tasks.pop())
                        # 启一个进程，去执行协程任务
                        p = Process(target=process_start, args=(tasks_list,))
                        p.start()
                    else:
                        tasks.append(url)
                        verify(url)
        else:
            print("NO:%s" % url)

if __name__ == '__main__':

    base_url = 'http://m.sohu.com/'
    verify(base_url)











