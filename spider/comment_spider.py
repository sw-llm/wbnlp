"""
    微博评论内容 爬虫代码 把微博评论信息存到csv文件
    https://weibo.com/ajax/statuses/buildComments?id=5187478260549274&is_show_bulletin=2
"""
import csv
import os
import time
from datetime import datetime

import requests

from util.stringUtil import clean_string


def init_csv():
    """
    初始化操作，判断csv文件是否存在，不能存在就创建一个
    :return:
    """
    if not os.path.exists('comment_data.csv'):  # 不存在就创建一个
        with open('comment_data.csv', 'w', encoding='utf8',
                  newline='') as file:  # newline=''参数，参数用于控制换行符的行为 这表示禁用自动换行符转换，即写入文件时使用原始的换行符（例如\r\n或\n）。这对于处理CSV文件时避免不必要的空行特别有用。
            writer = csv.writer(file)
            writer.writerow([
                'id',  # 评论信息id
                'text_raw',  # 评论内容
                'created_at',  # 创建日期
                'source',  # 发布位置 少部分没有这个值
                'like_counts',  # 点赞数
                'articleId',  # 微博id
                'userId',  # 评论用户id
                'userName',  # 评论用户名称
                'gender',  # 性别
                'userHomeUrl'  # 评论用户主页地址
            ])


def getAllArticleList():
    """
    获取所有微博信息
    :return:
    """
    articleList = []
    with open('article_data.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for article in csv_reader:
            articleList.append(article)
    return articleList


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


def writeToCsv(row):
    """
    写入csv操作 a操作 尾部追加 写入操作
    :param row:
    :return:
    """
    with open('comment_data.csv', 'a', encoding='utf8',
              newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)


def parseJson(json, articleId):
    """
    解析json数据
    :param json:
    :param articleId:
    :return:
    """
    commentList = json['data']
    for comment in commentList:
        id = comment['id']
        text_raw = clean_string(comment['text_raw'])
        created_at = datetime.strptime(comment['created_at'], "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d %H:%M:%S")
        source = comment.get('source', '来自').replace('来自', '').strip()
        like_counts = comment['like_counts']
        userId = comment['user']['id']
        userName = comment['user']['screen_name']
        gender = '男'
        g = comment['user']['gender']
        if g == 'f':
            gender = '女'
        userHomeUrl = 'https://weibo.com/u/%s' % comment['user']['id']

        writeToCsv([
            id,  # 评论信息id
            text_raw,
            created_at,
            source,
            like_counts,
            articleId,
            userId,
            userName,
            gender,
            userHomeUrl
        ])


def start():
    url = 'https://weibo.com/ajax/statuses/buildComments'
    init_csv()
    articleList = getAllArticleList()
    print("微博内容评论信息爬取开始")
    for article in articleList:
        print('正在爬取标题为：【%s】的微博评论数据' % article[1])
        time.sleep(1)
        params = {
            'id': article[0],
            'is_show_bulletin': 2
        }
        jsonHtml = getJsonHtml(url, params)
        if jsonHtml:
            parseJson(jsonHtml, article[0])
    print("微博内容评论信息爬取结束")


if __name__ == '__main__':
    start()
