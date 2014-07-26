#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import urllib
import urllib2
import re
import time
import socket
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    'Host':'www.douban.com',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Referer': 'www.douban.com/group/haixiuzu/',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4'
}
def get_html(url):
    content = urllib.urlopen(url).read().decode("utf-8")
    # req = urllib2.Request(url,None,headers)
    # content = urllib2.urlopen(req, None, 10)
    # print content.info()
    return content

def download_pic(num, page_num, url = "www.douban.com/group/haixiuzu/", path = "/home/lzs/pic/"):
    num25 = 25 * (page_num - 1)
    while num:
        num = num - 1
        reurl = url + 'discussion?start=' + str(num25)
        num25 = num25 + 25
        print "第" + str(page_num) + "页" + reurl 
        page_num = page_num + 1
        page_list, page_url_index = get_page_list(reurl)
        print "找到" + str(page_url_index) + "个标题"
        time.sleep(1)
        while page_url_index > 0:
            time.sleep(0.8)
            page_url_tuple = page_list[page_url_index]
            page_url_index = page_url_index - 1
            print page_url_tuple[3]
            pic_url_list, pic_index = get_pic_url(page_url_tuple[3])
            # fp = open("pic_url_list", "a+")
            while pic_index > 0:
                pic_url_tuple = pic_url_list[pic_index]
                pic_index = pic_index - 1
                pic_url = pic_url_tuple[3]
                print str(25 * (page_num - 2) + page_url_index) + "-" + str(pic_index) + "    " + pic_url
                # fp.write(pic_url + "\n")
                filename = urllib.urlretrieve(pic_url,'/Users/Pike/Documents/pic/%d-%d.jpg'%((25 * (page_num - 2) + page_url_index), pic_index))
                time.sleep(0.2)
            # fp.close()

def get_pic_url(url):
    pic_pattern = r'''<div([\s]+)class="topic-figure([\s]+)cc">([\s]+)<img src="([^"]+)" alt'''
    content = get_html(url)
    pic_url_list = re.findall(pic_pattern, content)
    return pic_url_list, len(pic_url_list) - 1

def get_page_list(url):
    page_pattern = r'''<td([\s]+)class="title">([\s]*)<a([\s]+)href="([^"]+)"'''
    content = get_html(url)
    page_list = re.findall(page_pattern, content)
    return page_list, len(page_list) - 1

def main():
    socket.setdefaulttimeout(10)
    print '#' * 90
    print "你可以什么都不输入，全部敲回车，默认下载<请不要害羞>小组的10页图片,但是要修改一下路径。代码35行"
    print "输入需要爬取的小组主页，如www.douban.com/group/haixiuzu/"
    url = raw_input('url:')
    print "存放路径,默认：/home/lzs/pic/"
    path = raw_input('path?:')
    print "需要爬取的页码，如10"
    num = raw_input('几页?:')
    print "从第几页开始爬爬爬？"
    page_num = raw_input('第几页开始 ?:')
    print '#' * 90
    url = "http://www.douban.com/group/haixiuzu/"
    if not num:
        num = 10
    if not page_num:
        page_num = 1
    num = int(num)
    page_num = int(page_num)
    # print get_html("http://www.baidu.com")
    rc = download_pic(num, page_num, url, path,)

if __name__ == "__main__":
    main()