#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Version: textLib,v 0.1
# FileName: textLib.py
# Date: <2014-08-22 >
# Description: 常用的文本函数库

import sys
import re
from htmlentitydefs import name2codepoint as n2cp


PUNCTUATIONS = u"!@#$%^&*()_+[];'\",./<>:！@#￥%……&*（）——+-=【】{}、|，。？、：；‘”“ ?~～～~《》?’ "
RE_HTML_ENTITY = re.compile(r'&(#?)(x?)(\w+);', re.UNICODE)


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if u'\u0030' <= uchar <= u'\u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    # if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
    if u'\u0041' <= uchar <= u'\u005a' or u'\u0061' <= uchar <= u'\u007a':
        return True
    else:
        return False


def is_al_num(uchar):
    """
    判断一个unicode是否是数字_或者英文字母
    :param uchar:
    :return:
    """
    if is_number(uchar) or is_alphabet(uchar) or uchar == u'_':
        return True
    else:
        return False


def is_numeric(input_str):
    """
    判断字符串是否是数值
    :param inputStr:
    :return:
    """
    return n_type_check(input_str, float)


def is_integer(input_str):
    """
    判断是否是整数
    :param inputStr:
    :return:
    """
    return n_type_check(input_str, long)


def n_type_check(input_str, n_type):
    try:
        n_type(input_str.strip())
        return True
    except ValueError:
        return False


def is_chinese_han(unicode_char):
    """
    判断字符是不是汉字
    :param unicode_char:
    :return:
    """
    # if unicodeChar >= u'\u4e00' and unicodeChar <= u'\u9fa5':
    if u'\u4e00' <= unicode_char <= u'\u9fa5':
        return True
    else:
        return False


def remove_html_symbol(original_text):
    """
    对文本中的html转义符号进行删除
    :param original_text:
    :return:
    """
    normal_text, num = re.subn(ur"&\w{2,4};", '', original_text)
    return normal_text


def tokenizer(original_text, to_lower=True):
    """
    对文本按照分割符进行切分
    :param original_text:
    :return : list of str
    """
    tmp_text = original_text
    result = []
    if not isinstance(original_text, unicode):
        tmp_text = unicode(original_text, "utf-8", "ignore").strip()
    if to_lower:
        tmp_text = tmp_text.lower()
    last_sen = ""
    for ch in tmp_text:
        if ch not in PUNCTUATIONS:
            last_sen += ch
        else:
            last_sen = last_sen.strip()
            if len(last_sen) >= 1:
                result.append(last_sen)
                last_sen = ""
    if len(last_sen.strip()) > 0:
        result.append(last_sen.strip())
    return result


def tokenizerFromSegResult(wordPosList):
    result = []
    tmp = []
    for word, pos in wordPosList:
        if pos != 'w':
            tmp.append((word, pos))
        else:
            if not tmp:
                if word == u"?" or word == u"？":
                    tmp.append((word, pos))
                result.append(tmp)
            tmp = []
    if not tmp:
        result.append(tmp)
    return result


def any2utf8(text, errors='strict', encoding='utf8'):
    """Convert a string (unicode or bytestring in `encoding`), to bytestring in utf8.
    """
    if isinstance(text, unicode):
        return text.encode('utf8')
        # do bytestring -> unicode -> utf8 full circle, to ensure valid utf8
    return unicode(text, encoding, errors=errors).encode('utf8')


def any2unicode(text, encoding='utf8', errors='strict'):
    """Convert a string (bytestring in `encoding` or unicode), to unicode."""
    if isinstance(text, unicode):
        return text
    return unicode(text, encoding, errors=errors)


def decodeHtmlEntity(text):
    """
    Decode HTML entities in text, coded as hex, decimal or named.
    @param text:
    @return:
    """
    def substitute_entity(match):
        ent = match.group(3)
        if match.group(1) == "#":
            # decoding by number
            if match.group(2) == '':
                # number is in decimal
                return unichr(int(ent))
            elif match.group(2) == 'x':
                # number is in hex
                return unichr(int('0x' + ent, 16))
        else:
            # they were using a name
            cp = n2cp.get(ent)
            if cp:
                return unichr(cp)
            else:
                return match.group()

    try:
        return RE_HTML_ENTITY.sub(substitute_entity, text)
    except:
        return text


def slide(content, width=2):
    return [content[i:i + width] for i in xrange(max(len(content) - width + 1, 1))]


def simple_tokenize(content):
    ucontent = content.strip()
    reg = ur'[\w\u4e00-\u9fff]+'
    if not isinstance(content, unicode):
        ucontent = unicode(content, "utf-8", "ignore").strip()
    ucontent = ucontent.lower()
    ucontent = ''.join(re.findall(reg, ucontent))
    ans = slide(ucontent)
    return ans

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")

    print is_integer('1341')
    print simple_tokenize('我是好人1234')

