# _*_coding:utf-8_*_
# Editor  : S YUAN
# Date    : 2019/5/15 20:12
# File    : index.py
# IDE     : PyCharm
from bs4 import BeautifulSoup
import urllib.request
import codecs
import requests
import time
import resource
import random
import urllib.parse
from mylog import MyLog as mylog

import pandas


class Item(object):
    top_num = None     # 排名
    score = None       # 得分
    mvName = None      # mv名字
    singer = None      # 歌手
    releasTime = None  # 发行时间


class getMvList(object):
    def __init__(self):
        self.urlBase = 'http://vchart.yinyuetai.com/vchart/trends?'
        self.areasDic = {'ML': '内地', 'HT': '港台', 'US': '美国', 'KR': '日本', 'JP': '日本'}
        self.log = mylog()
        self.geturls()

    def geturls(self):
        areas = ['ML', 'HT', 'US', 'KR', 'JP']
        pages = [str(i) for i in range(1, 4)]
        for area in areas:
            urls = []
            for page in pages:
                urlend = 'area=' + area + '&page=' + page
                url = self.urlBase + urlend
                urls.append(url)
                self.log.info(u'添加URL:%s 到URLS' % url)
            self.spider(area, urls)

    def getRseponseContent(self, url):
        proxy = urllib.request.ProxyHandler({'http': 'http://' + self.getRandomProxy()})
        opener = urllib.request.build_opener(proxy)
        urllib.request.install_opener(opener)
        try:
            res = requests.get(url, timeout=30, headers={'User-Agent': self.getRandomHeaders()})
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            # print(response.read().decode("utf-8"))
            time.sleep(1)
        except:
            self.log.error(u'Python 返回URL：%s 数据失败' % url)
        else:
            self.log.info(u'Python 返回URL:%s 数据成功' % url)
            return res.text

    def spider(self, area, urls):
        items = []
        for url in urls:
            responseContent = self.getRseponseContent(url)
            if not responseContent:
                continue
            soup = BeautifulSoup(responseContent, 'lxml')
            tags = soup.find_all('li', attrs={'name': 'dmvLi'})
            for tag in tags:
                item = Item()
                item.top_num = tag.find('div', attrs={'class': 'top_num'}).get_text()
                if tag.find('h3', attrs={'class': 'desc_score'}):
                    item.score = tag.find('h3', attrs={'class': 'desc_score'}).get_text()
                else:
                    item.score = tag.find('h3', attrs={'class': 'asc_score'}).get_text()
                item.mvName = tag.find('a', attrs={'class': 'mvname'}).get_text()
                item.singer = tag.find('a', attrs={'class': 'special'}).get_text()
                item.releasTime = tag.find('p', attrs={'class': 'c9'}).get_text()
                items.append(item)
                self.log.info(u'添加mvName为<<%s>>的数据成功' % (item.mvName))
        self.piplines(items, area)

    def getRandomProxy(self):
        return random.choice(resource.PROXIES)

    def getRandomHeaders(self):
        return random.choice(resource.UserAgents)

    def piplines(self, items, area):
        fileName = '音悦台top榜单.txt'
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        with codecs.open(fileName, 'a', 'utf8') as fp:
            fp.write('%s ------------------------------------------------------- %s\r\n' % (
            self.areasDic.get(area), nowTime))
            for item in items:
                fp.write('%s %s \t %s \t %s \t %s \r\n' % (
                item.top_num, item.score, item.releasTime, item.mvName, item.singer))
                self.log.info(u'添加mvName为<<%s>>的数据成功' % (item.mvName))
            fp.write('\r\n' * 4)


if __name__ == '__main__':
GML = getMvList()

