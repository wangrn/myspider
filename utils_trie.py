#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['Ahocorasick', 'AcTrie']

class Node(object):

    def __init__(self):
        self.next = {}
        self.fail = None
        self.isWord = False

class Ahocorasick(object):
    """
    Aho-corasick 算法实现
    """
    def __init__(self):
        self.__root = Node()

    def addWord(self, word):
        """
        添加关键词到Tire树中
        @param word: add word to Tire tree
        """
        tmp = self.__root
        for i in range(0, len(word)):
            if not tmp.next.has_key(word[i]):
                tmp.next[word[i]] = Node()
            tmp = tmp.next[word[i]]
        tmp.isWord = True

    def make(self):
        """
        build the fail function
        构建自动机，失效函数
        """
        tmpQueue = []
        tmpQueue.append(self.__root)
        while(len(tmpQueue) > 0):
            temp = tmpQueue.pop()
            p = None
            for k, v in temp.next.items():
                if temp == self.__root:
                    temp.next[k].fail = self.__root
                else:
                    p = temp.fail
                    while p is not None:
                        if p.next.has_key(k):
                            temp.next[k].fail = p.next[k]
                            break
                        p = p.fail
                    if p is None :
                        temp.next[k].fail = self.__root
                tmpQueue.append(temp.next[k])

    def search(self, content):
        """
        查找
        @param content:
        @return: list of tuple(startIndex,endIndex)
        """
        p = self.__root
        result = []
        startWordIndex = 0
        endWordIndex = -1
        currentPosition = 0

        while currentPosition < len(content):
            word = content[currentPosition]
            # 检索状态机，直到匹配
            while p.next.has_key(word) == False and p != self.__root:
                p = p.fail

            if p.next.has_key(word):
                if p == self.__root:
                    # 若当前节点是根且存在转移状态，则说明是匹配词的开头，记录词的起始位置
                    startWordIndex = currentPosition
                    # 转移状态机的状态
                p = p.next[word]
            else:
                p = self.__root

            if p.isWord:
                # 若状态为词的结尾，则把词放进结果集
                result.append((startWordIndex, currentPosition))

            currentPosition += 1
        return result

    def replace(self, content,replacement=u'*'):
        """
        替换
        @param replacement:
        @param content:
        """
        replacepos = self.search(content)
        result = content
        for i in replacepos:
            result = result[0:i[0]] + (i[1] - i[0] + 1) * replacement + content[i[1] + 1:]
        return result

class AcTrie(object):
    """
    工具类
    """
    def __init__(self,keyWordsInfo):
        """
        利用文件初始化
        @param keyWordsInfo: str或者是list or set of words，
        key文件位置文件格式：(keywords\s other) per line
        @return:
        """
        self.trie=Ahocorasick()
        if isinstance(keyWordsInfo,unicode) or isinstance(keyWordsInfo,str):
            fPath=keyWordsInfo
            for line in open(fPath,"r",True):
                items=line.decode("utf-8",'ignore').strip().split()
                if len(items)>=1:
                    self.trie.addWord(items[0])
        else:
            for word in keyWordsInfo:
                if not isinstance(word,unicode):
                    self.trie.addWord(unicode(word,"utf-8","ignore"))
                else:
                    self.trie.addWord(word)
        self.trie.make()

    def match(self,text):
        """
        @param text:
        @return: (matchedWordsList,textWithoutMatchedWords)
        """
        uText=text.strip()
        if not isinstance(text,unicode):
            uText=unicode(text,"utf-8","ignore").strip()
        indexList=self.trie.search(uText)
        keyWords=[]
        for startIndex,endIndex in indexList:
            keyWords.append(uText[startIndex:endIndex+1])
        return keyWords

    def replaceMatch(self,text,replacement=u" "):
        """
        查找并替换
        @param text:
        @return : (emotionStrList,textWithoutEmotion)
        """
        uText=text.strip()
        if not isinstance(text,unicode):
            uText=unicode(text,"utf-8","ignore").strip()
        indexList=self.trie.search(uText)
        keyWords=[]
        lastEndIndex=0
        parts=[]
        for startIndex,endIndex in indexList:
            keyWords.append(uText[startIndex:endIndex+1])
            parts.append(uText[lastEndIndex:startIndex].strip())
            lastEndIndex=endIndex+1
        if lastEndIndex<len(uText):
            parts.append(uText[lastEndIndex:].strip())
        textWithoutKeys=replacement.join(parts)
        return keyWords,textWithoutKeys


if __name__ == '__main__':
    ah = Ahocorasick()
    ah.addWord(u'测试')
    ah.addWord(u"我是")
    ah.make()
    print ah.search(u'测试123我是好人')
    print ah.replace(u'测试123我是好人')
