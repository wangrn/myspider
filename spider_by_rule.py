#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2014  Inc.
# Author:
# Version: dataCrawl,v 0.1
# FileName: dataCrawl.py
# Date: <2014-08-22 >
# Description: 

import lxml.etree as etree
import lxml.html.soupparser as soupparser
import urlparse
import urllib2
import uuid
import sys
import textLib
import traceback


class XpathDetail(object):
    def __init__(self, strValue):
        items = strValue.strip().split("`")
        if len(items) >= 3:
            self.valueType = int(items[0])

            self.path = items[1].strip()
            self.att = items[2].strip()

    def isValid(self):
        if self.path:
            return True
        else:
            return False


class Rule(object):
    '''
    描述各类型数据抓取的页面规则
    '''
    WORD_TYPE_PERSON = 0
    WORD_TYPE_ENTITY = 1
    VALUE_TYPE_TEXT = 0
    VALUE_TYPE_FILE = 1
    VALUE_TYPE_URL = 2


    @classmethod
    def itemDetailParse(self, strValue):
        """

        @param strValue:
        """
        index = strValue.find(":")
        if index > 0 and index + 1 < len(strValue):
            itemName = strValue[:index]
            pathChain = []
            pathChainStrs = strValue[index + 1:].split('^')
            for pathChainStr in pathChainStrs:
                if pathChainStr.strip():
                    pathDetail = XpathDetail(pathChainStr)
                    if pathDetail.isValid():
                        pathChain.append(pathDetail)
            return itemName, pathChain
        return None, None

    def __init__(self, line):
        """
        用一个字符串初始化一个规则
        @param line: str ,
            line 格式：wordType \t class1 \t class2 \t url \t termBaseXPath \t pageCoding \t {itemDetail1} \t {itemDetail2}
            itemDetail 格式：itemName:{pathChain}
            pathChain 格式：{path}^{path}
            path 格式：valueType`xpath`name
        eg：
        0   12  122 http://top.baidu.com/buzz?b=238 //*[@id="main"]/div[2]/div/table/tr gbk title:0`td[2]/a[1]`
        img:2`td[2]/a[1]`href^1`//*[@id="main"]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[1]/a/img`src
        """
        items = line.strip().split("\t")
        print items
        if len(items) >= 7:
            self.wordsType = items[0].strip()
            self.classId1 = items[1].strip()
            self.classId2 = items[2].strip()
            self.url = items[3].strip()
            self.termXpath = items[4]
            self.coding = items[5]
            self.itemDetail = dict()
            #print len(items)
            for item in items[6:]:
                itemName, pathChain = Rule.itemDetailParse(item)
                print itemName, pathChain
                if itemName and pathChain:
                    self.itemDetail[itemName] = pathChain
            self.valid = True
        else:
            self.valid=False


def fetchData(rule, tempFileSaveDir=""):
    '''
    根据给定的规则拉取数据
    @param rule:Rule
    @param tempFileDir:
    @return:
    '''
    result = []
    print "fetch :", rule.url, rule.itemDetail.keys()
    if not rule.valid:
        return result
    else:
        dom = getPageHtml(rule.url, pageCoding=rule.coding)
        if dom is None:
            return result
        for ele in dom.xpath(rule.termXpath):
            valueDict = dict()
            for itemName in rule.itemDetail:
                print "start fetch :", itemName, 50 * "*"
                curDom = ele
                pathChain = rule.itemDetail[itemName]
                for xpathDetail in pathChain:
                    value = getDataFromDom(curDom, xpathDetail)
                    print value
                    if value != None:
                        if xpathDetail.valueType == Rule.VALUE_TYPE_TEXT:
                            valueDict[itemName] = value.replace("\t"," ").replace("\r"," ").replace("\n"," ")
                            break
                        elif xpathDetail.valueType == Rule.VALUE_TYPE_FILE:
                            rIndex = value.rfind(".")
                            fileType = ".jpg"
                            if rIndex >= 0 and rIndex + 1 < len(value):
                                fileType = value[rIndex:]
                                if len(fileType) > 5:
                                    fileType = ".jpg"
                            saveName = str(uuid.uuid1()).replace("-", "") + fileType
                            #getFile(value, os.path.join(tempFileSaveDir, saveName))
                            valueDict[itemName] = saveName
                            break
                        elif xpathDetail.valueType == Rule.VALUE_TYPE_URL:
                            newUrl = value
                            if value.startswith("./"):
                                urlInfo = urlparse.urlparse(rule.url)
                                baseUrl = urlInfo.scheme + "://" + urlInfo.netloc
                                newUrl = baseUrl + newUrl[1:]
                            curDom = getPageHtml(newUrl, pageCoding=rule.coding)
            if len(valueDict) > 0: result.append(valueDict.items())
    return result


def getDataFromDom(dom, xpathDetail):
    if dom is None:
        return None
    path = xpathDetail.path
    att = xpathDetail.att.strip()
    itemDom = dom.xpath(path)
    if not itemDom:
        return None
    else:
        if not att:
            return itemDom[0].text_content()
        if att in itemDom[0].keys():
            return itemDom[0].get(att, "")
        elif att in etree.tostring(itemDom[0]):
            return getAttFromStr(att, etree.tostring(itemDom[0]))
        else:
            return None

def isValidXmlCharOrdinal(i):
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


def cleanXmlString(s):
    """
    清除字符串s中不符合xml规范的字符
    参考：http://stackoverflow.com/questions/8733233/filtering-out-certain-bytes-in-python
    @param s: unicode
    @return:unicode
    """
    return ''.join(c for c in s if isValidXmlCharOrdinal(ord(c)))



def getAttFromStr(att, line):
    """
    从字符串中获取属性信息
    @param att:
    @param line:
    @return:
    """
    attSymbol = " " + att + "="
    index = line.find(attSymbol)
    if index >= 0:
        tmpLine = line[index + len(attSymbol):].strip()
        symbol = tmpLine[0]
        symbolIndex = tmpLine.find(symbol, 1)
        if symbolIndex >= 1:
            tmpResult=tmpLine[1:symbolIndex]
            tmpResult=textLib.decodeHtmlEntity(tmpResult)
            return tmpResult
    return ""


def getPageHtml(url, enableProxy=True, parsed=True, pageCoding="utf-8"):
    '''
    获取指定的的页面，由soupparser进行转换，转换为htmlElement对象
    @param parsed: 是否进行转换
    @param url: 页面url
    @param enableProxy:是否启用代理
    @param pageCoding:页面编码
    @return:str if not parsed else lxml.html.htmlElement
    '''

    #proxyHandler = urllib2.ProxyHandler({"http":"http://10.130.145.102:80"})
    #noProxyHandler = urllib2.ProxyHandler({})
    #if enableProxy:
    #    opener = urllib2.build_opener(proxyHandler)
    #else:
    #    opener = urllib2.build_opener(noProxyHandler)
    #urllib2.install_opener(opener)
    pageContent = urllib2.urlopen(url).read()
    if not parsed:
        return pageContent
    if pageContent:
        if pageCoding:
            #print "coding", pageCoding
            pageContent = pageContent.decode(pageCoding, "ignore")
            #print pageContent
        pageContent = cleanXmlString(pageContent)
        # try:
        soup = soupparser.fromstring(pageContent)
        # except Exception as e:
        #     soup=None
        #     print "get page failed:",url
        #     traceback.print_stack()
        #     format_exception(e)
        return soup
    else:
        return None


def getFile(fileUrl, savePath, enableProxy=True):
    '''
    获取图片并保存
    @param fileUrl:
    @param savePath:文件保存位置
    @param enableProxy: 是否启动代理
    @return:
    '''
    print "get file:", fileUrl
    proxyHandler = urllib2.ProxyHandler({"http":"http://10.130.145.102:80"})
    noProxyHandler = urllib2.ProxyHandler({})
    if enableProxy:
        opener = urllib2.build_opener(proxyHandler)
    else:
        opener = urllib2.build_opener(noProxyHandler)
    urllib2.install_opener(opener)
    try:
        f = urllib2.urlopen(fileUrl)
        with open(savePath, "wb", True) as saveFile:
            saveFile.write(f.read())
    except:
        print "error while downloading file:", fileUrl


def getData(configFilePath, outputFilePath, fileSavingDir):
    """

    @param configFilePath:
    @param outputFilePath:
    @param fileSavingDir:文件保存位置
    @return:
    """
    rules = []
    for line in open(configFilePath, 'r', True):
        tmpLine = line.decode("utf-8", "ignore").strip()
        if tmpLine.strip() and tmpLine[0]!='#':
            rule = Rule(tmpLine)
            if rule and rule.valid:
                rules.append(rule)

    resultFile = open(outputFilePath, 'w', True)
    for rule in rules:
        print "new rule"
        result = fetchData(rule, fileSavingDir)
        outputHead = str(rule.wordsType) + "\t" + rule.classId1 + "\t" + rule.classId2
        if len(result):
            for item in result:
                outputTail = "\t".join(name + ":" + value.replace('\t', " ").replace('\r', " ") for name, value in item)
                resultFile.write(outputHead + "\t" + outputTail + "\n")
    resultFile.close()


def format_exception(e):
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    # Removing the last \n
    exception_str = exception_str[:-1]

    return exception_str


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")

    #if len(sys.argv) != 4:
        #printUsage(sys.argv[0])
    #    sys.exit(1)

    #conf,result,workdir = sys.argv[1],sys.argv[2], sys.argv[3]

    getData('./rebang.conf', 'output.txt', './')

