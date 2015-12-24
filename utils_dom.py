#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangruining'
import sys
import urllib2
import lxml.html.soupparser as parser
import lxml.etree as etree
import utils_xml
import utils_text

def fetch_html_page(url, page_coding='utf-8', parsed=True):
    page_content = urllib2.urlopen(url).read()
    if not parsed:
        return page_content
    if page_content:
        if page_coding:
            page_content = page_content.decode(page_coding, "ignore")
        page_content = utils_xml.clean_xml_string(page_content)
        dom = parser.fromstring(page_content)
        return dom
    else:
        return None


def get_attr_from_str(attr, line):
    """
    从字符串中获取属性信息
    @param att:
    @param line:
    @return:
    """
    attr_symbol = " " + attr + "="
    index = line.find(attr_symbol)
    if index >= 0:
        temp_line = line[index + len(attr_symbol):].strip()
        symbol = temp_line[0]
        symbol_index = temp_line.find(symbol, 1)
        if symbol_index >= 1:
            result = temp_line[1:symbol_index]
            result = utils_text.decodeHtmlEntity(result)
            return result
    return ""


def get_data_from_dom(dom, xpath, attr=None):
    if dom is None:
        return None
    item_dom = dom.xpath(xpath)
    if not item_dom:
        print 'error'
        return None
    else:
        if not attr:
            return item_dom[0].text_content()
        if attr in item_dom[0].keys():
            return item_dom[0].get(attr, "")
        elif attr in etree.tostring(item_dom[0]):
            return get_attr_from_str(attr, etree.tostring(item_dom[0]))
        else:
            return None
