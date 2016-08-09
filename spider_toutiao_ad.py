#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangrn'
import sys
import json
import utils_dom
import lxml.html.soupparser as parser
import utils_xml


"""
抓取今日头条的广告内容
"""

HEADER_DICT = dict()
HEADER_DICT['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.2.2; GT-I9505 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'
HEADER_DICT['X-Requested-With'] = 'XMLHttpRequest'
HEADER_DICT['Cookie'] = 'uuid="w:a0e985b387f848dbba3c45658564def9"; tt_webid=10553455390; _ga=GA1.2.1523828940.1453721900; __utma=24953151.1523828940.1453721900.1454297969.1455524918.4; __utmc=24953151; __utmz=24953151.1454046743.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; utm_source=toutiao; csrftoken=8a350207cb9babcd07685460251d65cb'


def main():
    url = 'http://m.toutiao.com/list/?tag=__all__&ac=wap&item_type=4&count=50&format=json&list_data_v2=1&min_behot_time=1455534412&ad_pos=4&ad_gap=6&csrfmiddlewaretoken=8a350207cb9babcd07685460251d65cb'
    json_content = utils_dom.fetch_html_page(url, page_coding='UTF-8', parsed=False, headers=HEADER_DICT)
    obj = json.loads(json_content)
    html_content = obj[u'html'].replace('\n', '')
    html_content = utils_xml.clean_xml_string(html_content)
    print html_content
    dom = parser.fromstring(html_content)

    for ele in dom.xpath('section[@data-id]'):
        try:
            is_ad = utils_dom.get_data_from_dom(ele, 'i/img', 'ad-label')
            if is_ad:
                title = utils_dom.get_data_from_dom(ele, 'a/div/h3')
                if title is None:
                    title = utils_dom.get_data_from_dom(ele, 'a/h3')
                campany = utils_dom.get_data_from_dom(ele, 'a/div/div[@class="item_info"]/span[@class="src space"]')
                if campany is None:
                    campany = utils_dom.get_data_from_dom(ele, 'a/div[@class="item_info"]/span[@class="src space"]')
                landing_page = utils_dom.get_data_from_dom(ele, 'a', 'href')
                #if title is not None:
                print title, landing_page, campany
        except:
            pass

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    main()
