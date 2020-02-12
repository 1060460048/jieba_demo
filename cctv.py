#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import logging
import codecs
import json
import time,datetime
import re
from pymongo import MongoClient
import sys
from lxml import etree
from lxml import html
from urllib.parse import urlparse



MONGO_URI = 'localhost'

MONGO_DATABASE = 'cctv'

client=MongoClient('127.0.0.1',27017)
db=client['cctv']

collection=db['daynews1']


CRAWL_START=False
if CRAWL_START:
    #获取到当前时间
    dt=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # logger = logging.getLogger(__name__)

    LOG_FILENAME='test.log'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1; Mi A1 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36',
    }

    def logger(msg):
        # logging.info('\n')
        logging.info('\n'+str(dt)+'>>>>>>>>>>>>>>>:'+msg)

    def listToString(s):
        # initialize an empty string
        str1 = ""

        # traverse in the string
        for ele in s:
            str1 += ele

            # return string
        return str1

    print('程序开始执行')
    start_time=datetime.datetime.now()
    logging.info('>>>>>开始执行时间'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    for i in range(1,8,1):
        url='http://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/china_%d.jsonp?cb=t&cb=chin' % (i)
        # logger(url)
        res=requests.get(url,headers=headers)


        res.encoding = 'utf-8'

        res=str(res.text.replace('china','',1))
        # res=json.dumps(res)
        # json_data=json.loads(res)

        pattern=re.compile('\((.*)\)')
        matches=re.search(pattern,res)

        bbb=eval(matches.group(1))

        data_list = bbb['data']['list']

        insert_list_data = []

        for elem in data_list:
            logger(elem['url'])
            inner_url = elem['url']
            if inner_url:
                urlarray = urlparse(inner_url)
                netloc = urlarray[1] if urlarray[1] else ''
                if "news" not in netloc or netloc == '':
                    logging.info('不是news，请检查')
                    continue

                res = requests.get(inner_url)
                res = html.fromstring(res.content)
                aaa = etree.tostring(res)

                insert_data = {}
                h1 = res.xpath('//h1/text()')[0]
                h1 = h1.__str__()

                try:
                    content = res.xpath('//div[@class="content_area"]//text()')
                    content = listToString(content)
                    content = content.strip()
                    if not content:
                        continue
                    editor = res.xpath('//div[@class="zebian"]//text()')
                    editor_string = listToString(editor).strip()
                    editor_string = editor_string.replace("\r\n", "|").replace(" ", "")
                    info = res.xpath('//div[@class="info1"]//text()')[0]
                    info = info.__str__()
                    logging.info(info)
                    if info:
                        info_res = info.split('|')
                        created_by = info_res[0] if info_res[0] else ''
                        array = time.strptime(str(info_res[1]).lstrip(" "), u"%Y年%m月%d日 %H:%M")
                        created_at = int(time.mktime(array)) if array else ''
                    else:
                        created_by = ''
                        created_at = ''
                except Exception as e:
                    content = res.xpath('//div[@id="text_area"]//text()')
                    content = listToString(content)
                    content = content.strip()
                    if not content:
                        continue
                    editor = res.xpath('//div[@class="relevance"]//text()')
                    editor_string = listToString(editor).strip()
                    editor_string = editor_string.replace("\r\n", "|").replace(" ", "")
                    info = res.xpath('//span[@class="info"]//i[1]//text()')
                    if info:
                        created_by = info[1] if info[1] else ''
                        array = time.strptime(str(info[2]).lstrip(" "), u"%Y年%m月%d日 %H:%M")
                        created_at = int(time.mktime(array)) if array else ''
                    else:
                        created_by = ''
                        created_at = ''
                finally:
                    logging.info('无处理规则，请检查，当前处理的url是：' + str(test_url))

                insert_data = {'title': h1, 'url':inner_url, 'content': content, 'editor': editor_string, 'created_by': created_by,'created_at': created_at}

                logging.info(insert_data)
                insert_list_data.append(insert_data)
                logging.info(insert_list_data)

        if insert_list_data:
            collection.insert_many(insert_list_data,ordered=False)
            print('>>>>插入数据库成功，入库数据条数：'+str(len(insert_list_data)))
        else:
            pass

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    logging.info('>>>>>结束执行时间' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print('程序总共执行时间为：')
    print(duration)

import jieba_fast as jieba
import jieba.analyse
import jieba.posseg as pseg
import codecs,sys,os
from string import punctuation
from pathlib import Path
from os import path
import collections
import numpy as np
import wordcloud
from PIL import Image
import matplotlib.pyplot as plt
from contextlib import ExitStack
from itertools import zip_longest


class Statistics(object):

    def __init__(self):
        self.connection=MongoClient('127.0.0.1',27017)
        self.db=self.connection.cctv
        self.collection=self.db.daynews1


    def get_all(self):
        return self.collection.find()

    def extract_one(self,file=None):
        add_punc = '，。、【 】 “”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=&#@￥'
        all_punc = punctuation + add_punc
        ins = Statistics()

        path_str = Path(file)
        if not path_str.exists() or not path_str.is_file():
            data_list = self.get_all()
            large_text = ''
            for item in data_list:
                large_text += str(item['content'])
            codecs.open("test1.txt", 'w', encoding="utf-8").write(large_text)
            print('执行完毕')

        print('打开文件')
        f = codecs.open(file, 'r+', encoding='utf-8')
        line_number = 1
        line = f.readline()
        while line:
            print('----->>>>>执行', line_number, ' -------------')
            line_seg = " ".join(jieba.cut(line))
            test_line = line_seg.split(' ')
            res = []
            for elem in test_line:
                res.append(elem)
                if elem in all_punc:
                    res.remove(elem)

            line_seg2 = " ".join(jieba.cut(''.join(res)))
            target = codecs.open('output1.txt', 'w+', encoding='utf-8')
            target.writelines(line_seg2)
            line_number = line_number + 1
            line = f.readline()
        f.close()
        target.close()
        exit()

    def parse_multiple_files1(self,flist=[]):
        output=[]
        with ExitStack() as stack:
            files=[stack.enter_context(codecs.open(fname,'r+',encoding='utf-8')) for fname in flist]
            print(files)
            for lines in zip_longest(*files):
                output.append(str(lines).replace('\r\n',''))
        exit()

        return output

    def parse_multiple_files(self,flist=[]):
        output=[]
        if flist:
            for item in flist:
                fp=codecs.open(item,'r+',encoding='utf-8')
                wordlist=fp.readlines()
                for word in wordlist:
                    output.append(word.strip())
            return output
        else:
            return []



    def extract_two(self,file=None):
        fn=codecs.open(file,'r+',encoding='utf-8')
        string_data=fn.read()
        fn.close()

        # 文本预处理
        pattern = re.compile('[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~。“”、：？，【】！（）——↓0-9a-zA-Z\.\.\.\.\.\.]+')
        # pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')
        string_data = re.sub(pattern, '', string_data)  # 将符合模式的字符去除
        string_data = string_data.replace('\n', '')
        string_data = string_data.replace('\u3000', '')
        string_data = string_data.replace('\r', '')
        string_data = string_data.replace(' ', '')
        logging.info(string_data)

        # 文本分词
        seg_list_exact = jieba.cut(string_data, cut_all=False)  # 精确模式分词
        object_list = []
        remove_words_custom = [u'的', u'，', u'和', u'是', u'随着', u'对于', u'对', u'等', u'能', u'都', u'。',
                        u' ', u'、', u'中', u'在', u'了', u'通常', u'如果', u'我们', u'需要',u'月',u'日']  # 自定义去除词库
        remove_words = self.parse_multiple_files(['中文停用词表.txt','哈工大停用词表.txt','四川大学机器智能实验室停用词库.txt','百度停用词表.txt'])
        remove_words=remove_words_custom+remove_words
        for word in seg_list_exact:  # 循环读出每个分词
            if word not in remove_words:  # 如果不在去除词库中
                logging.info('\n')
                logging.info(word)
                object_list.append(word)  # 分词追加到列表
        logging.info(object_list)

        # 词频统计
        word_counts = collections.Counter(object_list)  # 对分词做词频统计
        word_counts_top10 = word_counts.most_common(10)  # 获取前10最高频的词
        print(word_counts_top10)  # 输出检查
        # 词频展示
        font_path=r'C:\Windows\Fonts\simfang.ttf'
        mask = np.array(Image.open('background.jpg')) # 定义词频背景
        wc = wordcloud.WordCloud(
            background_color='white', # 设置背景颜色
            font_path=font_path, # 设置字体格式
            mask=mask, # 设置背景图
            max_words=200, # 最多显示词数
            max_font_size=200 , # 字体最大值
            scale=80  # 调整图片清晰度，值越大越清楚
        )
        wc.generate_from_frequencies(word_counts)  # 从字典生成词云
        image_colors = wordcloud.ImageColorGenerator(mask)  # 从背景图建立颜色方案
        wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
        plt.figure()
        plt.imshow(wc)  # 显示词云
        plt.axis('off')  # 关闭坐标轴
        plt.show()  # 显示图像
        wc.to_file("bb.jpg")  # 将图片输出为文件



if __name__ == '__main__':
    ins=Statistics()
    ins.extract_two('test1.txt')
    # ins.extract_one('test1.txt')




