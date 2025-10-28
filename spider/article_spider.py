"""
    微博内容爬取，以及存csv文件
    https://weibo.com/ajax/feed/hottimeline?group_id=1028032222&containerid=102803_2222&extparam=discover%7Cnew_feed
"""
import csv
import os
import time
from datetime import datetime

import requests

from util.stringUtil import clean_string


def init_csv():
    """
    初始化操作，判断csv文件是否存在，不存在就创建一个
    :return:
    """
    if not os.path.exists('article_data.csv'):  # 存在则创建一个
        with open('article_data.csv', 'w', encoding='utf8',
                  newline='') as file:  # newline=''参数，参数用于控制换行符的行为 这表示禁用自动换行符转换，即写入文件时使用原始的换行符（例如\r\n或\n）。这对于处理CSV文件时避免不必要的空行特别有用。
            writer = csv.writer(file)
            writer.writerow([
                'id',  # 帖子id
                'text_raw',  # 内容
                'reposts_count',  # 转发总数
                'comments_count',  # 评论总数
                'attitudes_count',  # 点赞总数
                'region_name',  # 发布位置 少部分没有这个值
                'created_at',  # 创建日期
                'articleType',  # 帖子类型
                'articleUrl',  # 帖子地址   https://weibo.com/userid/mblogid
                'authorId',  # 用户id
                'authorName',  # 用户名称
                'authorHomeUrl'  # 用户主页地址
            ])


def getJsonHtml(url, params):
    """
    请求获取html内容，json数据格式
    :param url:
    :param params:
    :return:
    """
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        'cookie': "UOR=www.baidu.com,s.weibo.com,www.baidu.com; SINAGLOBAL=147269028916.96313.1738405722917; SCF=Aq_smbP0Qulm3aIQiWHRj0MVjLlLvMzPjh08C1UOgzZGKmgtkj3RlIKkPpPunA-Yp4Vs3PxaE2Mnw4EfY-zo22k.; ULV=1746148684228:3:1:1:750370364305.8235.1746148684180:1743395262982; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWdhwhTipHbo3gGv6wzaRcu5JpX5KMhUgL.Foef1hMR1KqEeoz2dJLoI08ZqP9yi--NiKLsi-2fi--Ri-8siKnci--fiKnRiKnci--Xi-iWi-8Fi--Ni-i2iK.p; ALF=1754794282; SUB=_2A25FdAx5DeRhGeVL41UZ-SjOyT6IHXVmCAGxrDV8PUJbkNAbLWfskW1NTBTNHVQQjZ8TTBpAQ68hUItVd4KUD_CC; XSRF-TOKEN=-13mbOvaiCqG7D10Nh7BXDT9; WBPSESS=_IA_wwSTTkx7cB4s0X9svEMSaQHgjmYl9nytbvfrAce3eyBsA23XYXjJftuXIH_8zgKW2oqqiIJoisfr9IyvPWruJf1IO1Uz6X6EnrXkNTqTD9D7usdZBbo-25n3r_SLjL3lkCtntbri1Bywm6wKdA=="
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def getAllTypeList():
    """
    获取所有微博类别信息
    :return:
    """
    allTypeList = []
    with open('arcType_data.csv', 'r', encoding='utf8',
              newline='') as file:  # newline=''参数，参数用于控制换行符的行为 这表示禁用自动换行符转换，即写入文件时使用原始的换行符（例如\r\n或\n）。这对于处理CSV文件时避免不必要的空行特别有用。
        reader = csv.reader(file)
        next(reader)
        for articleType in reader:
            allTypeList.append(articleType)
    return allTypeList


def writeToCsv(row):
    """
    写入csv操作 a 追加 写入
    :param arcType:
    :return:
    """
    with open('article_data.csv', 'a', encoding='utf8',
              newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)


def parseJson(json, articleType):
    """
    解析Json数据
    :param json:
    :param json:
    :return:
    """
    articleList = json['statuses']
    for article in articleList:
        id = article['id']
        text_raw = clean_string(article['text_raw'])
        reposts_count = article['reposts_count']
        comments_count = article['comments_count']
        attitudes_count = article['reposts_count']
        region_name = article.get('region_name', '发布于').replace('发布于', '').strip()
        created_at = datetime.strptime(article['created_at'], "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d %H:%M:%S")
        articleUrl = 'https://weibo.com/%s/%s' % (article['user']['id'], article['mblogid'])
        authorId = article['user']['id']
        authorName = article['user']['screen_name']
        authorHomeUrl = 'https://weibo.com/u/%s' % article['user']['id']

        writeToCsv([
            id,
            text_raw,
            reposts_count,
            comments_count,
            attitudes_count,
            region_name,
            created_at,
            articleType,
            articleUrl,
            authorId,
            authorName,
            authorHomeUrl
        ])


def start():
    url = 'https://weibo.com/ajax/feed/hottimeline'
    init_csv()
    allTypeList = getAllTypeList()
    print(allTypeList)
    print("微博内容爬取开始")
    for articleType in allTypeList:
        print('正在爬取类型为：【%s】的微博数据' % articleType[0])
        time.sleep(1)
        params = {
            'group_id': articleType[1],
            'containerid': articleType[2],
            'extparam': 'discover|new_feed'
        }
        jsonHtml = getJsonHtml(url, params)
        parseJson(jsonHtml, articleType[0])
    print("微博内容爬取结束")


if __name__ == '__main__':
    """
    https://weibo.com/ajax/feed/hottimeline?group_id=1028032222&containerid=102803_2222&extparam=discover%7Cnew_feed
    """
    start()
