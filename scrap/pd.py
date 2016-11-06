# -*- coding:utf-8 -*-
import re
import urllib, urllib2


# 获取网页源码
def gethtml(url):
    hearder = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
               'Referer': '******'}
    request = urllib2.Request(url, headers=hearder)
    papg = urllib2.urlopen(request)  # ('http://www.wmpic.me/meinv')
    html = papg.read()
    return html


x = 0


def getimg(html):
    imgre = re.compile(r' src="(.*?)" class=')
    imglist = re.findall(imgre, html)  # 返回的列表
    global x
    for imgurl in imglist:
        print imgurl
        urllib.urlretrieve(imgurl, 'C:\Users\LEO\Desktop\meizi\%s.jpg' % x)
        x += 1
        print("正在下载第%s张" % x)


def main():
    for i in range(1, 19):
        url = "http://www.wmpic.me/meinv/page/%s" % i
        html = gethtml(url)
        getimg(html)


if __name__ == '__main__':
    main()
