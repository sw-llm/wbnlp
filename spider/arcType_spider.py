"""
    https://weibo.com/ajax/feed/allGroups
    微博类别信息爬取 存csv文件
"""
import csv
import os.path

import numpy as np
import requests


def init_csv():
    """
    初始化操作，判断csv文件是否存在，不存在就创建一个
    :return:
    """
    if not os.path.exists('arcType_data.csv'):  # 存在则创建一个
        with open('arcType_data.csv', 'w', encoding='utf8',
                  newline='') as file:  # newline=''参数，参数用于控制换行符的行为 这表示禁用自动换行符转换，即写入文件时使用原始的换行符（例如\r\n或\n）。这对于处理CSV文件时避免不必要的空行特别有用。
            writer = csv.writer(file)
            writer.writerow([
                '类别标题(title)',
                '分组id(gid)',
                '分类id(containerid)'
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


def writeToCsv(row):
    """
    写入csv操作 a 追加 写入
    :param arcType:
    :return:
    """
    with open('arcType_data.csv', 'a', encoding='utf8',
              newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)


def parseJson(json):
    """
    解析Json数据
    :param json:
    :return:
    """
    arcTypeList = np.append(json['groups'][3]['group'], json['groups'][4]['group'])
    print(arcTypeList)
    for arcType in arcTypeList:
        arcType_title = arcType['title']
        gid = arcType['gid']
        containerid = arcType['containerid']
        writeToCsv([arcType_title, gid, containerid])


def start():
    init_csv()
    url = "https://weibo.com/ajax/feed/allGroups"
    jsonHtml = getJsonHtml(url, {})
    print(jsonHtml)
    parseJson(jsonHtml)


if __name__ == '__main__':
    start()
