"""
     爬数据，持久化到数据库 主函数
"""
import os
import traceback

import pandas as pd
from sqlalchemy import create_engine

from article_spider import start as articleSpiderStart
from comment_spider import start as commentSpiderStart

engine = create_engine('mysql+pymysql://root:123456@localhost:3308/db_weibo3?charset=utf8mb4')


def dataClean():
    """
    数据清洗，对csv文件数据库，pandas库处理
    :return:
    """
    pass


def saveToDb():
    """
    持久化到数据库，先合并数据库和csv文件，再去重，然后存数据库，最后删除csv文件
    :return:
    """
    try:
        oldArticleDb = pd.read_sql('select * from t_article', engine)
        newArticleCsv = pd.read_csv('article_data.csv')
        concatArticlePd = pd.concat([newArticleCsv, oldArticleDb])
        resultArticlePd = concatArticlePd.drop_duplicates(subset='id', keep='last')
        resultArticlePd.to_sql('t_article', con=engine, if_exists='replace', index=False)

        oldCommentDb = pd.read_sql('select * from t_comment', engine)
        newCommentCsv = pd.read_csv('comment_data.csv')
        concatCommentPd = pd.concat([newCommentCsv, oldCommentDb])
        resultCommentPd = concatCommentPd.drop_duplicates(subset='id', keep='last')
        resultCommentPd.to_sql('t_comment', con=engine, if_exists='replace', index=False)
    except Exception as e:
        print('异常：', e)
        traceback.print_exc()
        newArticleCsv = pd.read_csv('article_data.csv')
        newCommentCsv = pd.read_csv('comment_data.csv')
        newArticleCsv.to_sql('t_article', con=engine, if_exists='replace', index=False)
        newCommentCsv.to_sql('t_comment', con=engine, if_exists='replace', index=False)

    os.remove('article_data.csv')
    os.remove('comment_data.csv')


if __name__ == '__main__':
    print("微博内容爬取开始...")
    articleSpiderStart()
    print("微博内容爬取结束...")

    print("微博评论信息爬取开始...")
    commentSpiderStart()
    print("微博评论信息爬取结束...")

    print("数据清洗开始...")
    dataClean()
    print("数据清洗结束...")

    print("微信内容和评论信息持久化到数据库开始...")
    saveToDb()
    print("微信内容和评论信息持久化到数据库结束...")
