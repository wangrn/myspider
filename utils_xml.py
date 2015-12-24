#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'donhu'
import sys


def is_valid_xml_char_ordinal(i):
    """
    判断字符是不是xml的合法字符
    XML standard defines a valid char as::
    Char ::= #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]
    @param i: unicode char
    @return:True if valid else False
    """
    return (
        0x20 <= i <= 0xD7FF
        or i in (0x9, 0xA, 0xD)
        or 0xE000 <= i <= 0xFFFD
        or 0x10000 <= i <= 0x10FFFF
    )


def clean_xml_string(s):
    """
    清除字符串s中不符合xml规范的字符
    参考：http://stackoverflow.com/questions/8733233/filtering-out-certain-bytes-in-python
    @param s: unicode
    @return:unicode
    """
    return ''.join(c for c in s if is_valid_xml_char_ordinal(ord(c)))


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

