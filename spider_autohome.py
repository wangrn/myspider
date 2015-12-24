#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangrn'
import sys
import utils_dom

domain = 'http://car.autohome.com.cn'


def top_car_brand(output_stream=sys.stdout):
    # 抓取热门汽车品牌
    top_brand = list()
    url = 'http://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1&brandId=0&fctId=0&seriesId=0'
    dom = utils_dom.fetch_html_page(url, page_coding='gb2312')
    for element in dom.xpath('//ul/li/h3/a'):
        name_cnt = utils_dom.get_data_from_dom(element, '.')
        name, cnt = name_cnt.split('(')
        cnt = cnt[:-1]
        href = domain + utils_dom.get_data_from_dom(element, '.', 'href')
        output_stream.write(name + '\t' + cnt + '\t' + href + '\n')
        top_brand.append((name, cnt, href))
    return top_brand


def fetch_car_type(car_brand, output_stream=sys.stdout):
    # 抓取各品牌的具体车型号
    # top_brand = [(brand, cnt, url)]

    for (brand, cnt, url) in car_brand:
        series_cnt = 0
        dom = utils_dom.fetch_html_page(url, page_coding='gb2312')
        for element in dom.xpath('//div[@class="carbradn-cont fn-clear"]/dl'):
            sub_brand = utils_dom.get_data_from_dom(element, 'dt/a')
            series_type = ''
            for ele in element.xpath('dd/div'):
                dom_type = utils_dom.get_data_from_dom(ele, '.', 'class')
                if dom_type == 'list-dl-name':
                    series_type = utils_dom.get_data_from_dom(ele, '.').replace('：', '')
                else:
                    for e in ele.xpath('a'):
                        series_name = utils_dom.get_data_from_dom(e, '.')
                        series_url = domain + utils_dom.get_data_from_dom(e, '.', 'href')
                        if series_name.find('停售') != -1:
                            continue
                        series_cnt += 1
                        output_stream.write('\t'.join([brand, sub_brand, series_type, series_name, series_url]) + '\n')
        print brand, cnt, series_cnt

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    car_brand = top_car_brand(output_stream=file('./data/car_brand.txt', 'w'))
    fetch_car_type(car_brand, output_stream=file('./data/series_info.txt', 'w'))

