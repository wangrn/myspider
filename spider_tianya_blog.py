#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangrn'
import sys
import utils_dom


class TianyaBlogSpider(object):
    def __init__(self, output_stream=sys.stdout, list_page_url=None, ):
        self.list_page_url = list_page_url
        self.output_stream = output_stream
        self.content_url_list = []

    def run(self):
        for page_index in range(1, 6):
            url = self.list_page_url + str(page_index) + '.shtml'
            print url
            self._get_content_url(url)

        for item in self.content_url_list[::-1]:
            print item[0], item[1]
            self._get_content(item[1], self.output_stream)

    def _get_content_url(self, url):
        dom = utils_dom.fetch_html_page(url, page_coding='UTF-8')
        for ele in dom.xpath('//*[@class="bloglistwrapper"]/li'):
            anchor, link = utils_dom.get_data_from_dom(ele, 'p[1]/a'), utils_dom.get_data_from_dom(ele, 'p[1]/a', 'href')
            if anchor is None or link is None:
                continue
            self.content_url_list.append((anchor, link))

    @staticmethod
    def _get_content(url, output_stream=sys.stdout):
        dom = utils_dom.fetch_html_page(url, page_coding='UTF-8')
        title = utils_dom.get_data_from_dom(dom, '//*[@id="right_bigcontent"]/div/div[2]/div[1]/h2/a')
        content = utils_dom.get_data_from_dom(dom, '//*[@id="right_bigcontent"]/div/div[2]/div[1]/div[2]')\
            .replace('　　　　', '\n\n').strip()
        output_stream.write('<<' + title + '>>' + '\n')
        output_stream.write(content + '\n')
        output_stream.write('\n\n' + '--------------------------------------------------------------------------------'
                            + '\n\n')

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    spider = TianyaBlogSpider(output_stream=open('./result.txt', 'w'),
                              list_page_url='http://blog.tianya.cn/listcate-1554014-2321439-')
    spider.run()