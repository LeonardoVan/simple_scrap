# coding:utf-8

import urllib2
import re
import HTMLParser  # 解析
import sys

reload(sys)
sys.setdefaultencoding('utf-8')  # 输入文件内容的编码格式


# 通过请求获取HTML
def get_html(url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
              'Referer': '******'}  # 伪装成浏览器访问网站，避免反爬虫
    request = urllib2.Request(url, headers=header)
    response = urllib2.urlopen(request)
    text = response.read()
    return text


# 解析链接
def get_urls(html):
    pattern = re.compile('http://daily.zhihu.com/story/(.*?)"', re.S)  # 编译正则表达式，提高爬取效率
    items = re.findall(pattern, html)  # 返回地址列表
    urls = []
    for item in items:
        urls.append('http://daily.zhihu.com/story/' + item)
    return urls


# 解析内容
def get_count(url):
    html = get_html(url)  # 获取源代码
    pattern = re.compile('<h1 class="headline-title">(.*?)</h1>', re.S)
    items = re.findall(pattern, html)
    print '*****' + items[0] + '*****'

    pattern = re.compile('<div .*?"content">(.*?)</div>', re.S)
    items_withtag = re.findall(pattern, html)
    for item in items_withtag:
        for content in characterProcessing(item):
            print content


# 去除文章中多余的标签
def characterProcessing(html):
    htmlParser = HTMLParser.HTMLParser()
    pattern = re.compile('<p>(.*?)</p>|<li>(.*?)</li>.*?', re.S)
    items = re.findall(pattern, html)
    result = []
    for index in items:
        if index != '':
            for content in index:
                tag = re.search('<.*?>', content)
                http = re.search('<.*?http.*?', content)
                html_tag = re.search('&', content)
                if html_tag:  # 处理html转义符
                    content = htmlParser.unescape(content)
                # 遇到链接时，直接跳过不做抓取
                if http:
                    continue
                elif tag:
                    pattern = re.compile('(.*?)<.*?>(.*?)</.*?>(.*)')
                    items = re.findall(pattern, content)
                    content_tags = ''
                    if len(items) > 0:
                        for item in items:
                            if len(item) > 0:
                                for item_s in item:
                                    content_tags = content_tags + item_s
                            else:
                                content_tags = content_tags + item_s
                        content_tags = re.sub('<.*?>', '', content_tags)
                        result.append(content_tags)
                    else:
                        continue
                else:
                    result.append(content)
    return result


def main():
    for i in range(1, 5):
        print '正在查看第%s页' % i
        url = "http://zhihudaily.ahorn.me/page/%s" % i
        html = get_html(url)
        urls = get_urls(html)
        for url in urls:
            try:
                get_count(url)
            except Exception, e:
                print e

if __name__ == "__main__":
    main()
