"""
    微博评论信息 数据访问对象
"""
from util import dbUtil


def getAllComment():
    """
    获取所有评论信息
    :return:
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = "SELECT * FROM t_comment WHERE text_raw!=''"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)


def getTopCommentUser():
    """
    获取TOP前50评论用户名
    :return:
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = "SELECT username,COUNT(username) AS unCount FROM t_comment GROUP BY username ORDER BY unCount DESC LIMIT 0,50"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)


def getCommentAmount():
    """
    获取7天用户评论量
    :return:
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = "SELECT DATE_FORMAT(created_at,'%Y-%m-%d') AS commentDate,COUNT(text_raw) AS commentTotal FROM t_comment GROUP BY commentDate ORDER BY commentDate DESC LIMIT 0,7"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)


def getCommentHotWordAmount(hotword):
    """
    获取日期用户热词评论量
    :return:
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = f"SELECT DATE_FORMAT(created_at,'%Y-%m-%d') AS commentDate,COUNT(text_raw) AS commentTotal FROM t_comment WHERE LOCATE('{hotword}',text_raw)>0  GROUP BY commentDate ORDER BY commentDate DESC "
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)


def getCommentByHotWord(hotword):
    """
    根据热词查询评论信息
    :return:
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = f"SELECT * FROM t_comment WHERE LOCATE('{hotword}',text_raw)>0"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)
