#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangrn'
import sys


class BaikeSpider(object):
    """
    抓取百度的对应关键词的页面, 从中解析出需要字段.
    """
    def __init__(self, keywords=[]):
        self.keywords = keywords

    def run(self):

        pass


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    spider = BaikeSpider(keywords=[line.strip() for line in file('./baidu.word.txt')])
    spider.run()

