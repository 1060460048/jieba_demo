疫情之下，看权威发布的央视发布的信息集全民之力，每天发表的新闻中的关键信息是哪些，于是动手写了这个脚本；
# 使用方法
#### 1.把文件[cctv.py]中的CRAWL_START=False改成True，并连上自己的本地mongodb数据库，可以把数据采集完成并写入mongodb数据库；
#### 2.然后将CRAWL_START=False改成False,然后运行脚本即可看到效果；
<font color=red>注意:本文使用的dom解析器是lxml.etree组件的xpath方法来解析dom，并对news.cctv.com新闻页面页面结构做了兼容，没用BeautifulSoup是性能 考虑，没用regex，觉得用xpath更有通用性，仅做抛砖引玉的作用，如有问题，还请指正。如遇到问题可以联系我qq：１０６０４６００４８</font>
##### 中文常用停用词表（脚本中使用的停用词表，感谢辛苦整理的作者）
- 中文停用词表.txt
- 哈工大停用词表.txt
- 百度停用词表.txt
- 四川大学机器智能实验室停用词库.txt
最终效果

![](http://q4xj8j4yk.bkt.clouddn.com//img/Figure_3.png)

# 春暖花开，疫情消散，武汉加油，中国加油！


