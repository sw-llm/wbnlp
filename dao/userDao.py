"""
    用户数据访问对象
"""
from entity.UserModel import User
from util import dbUtil


def login(user: User):
    """
    登录判断
    :param user: 
    :return: 
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM t_user WHERE username='{user.username}' and password='{user.password}'")
        return cursor.fetchone()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)


def add(user: User):
    """
    用户注册添加
    :param user:
    :return:
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(f"insert into t_user values(null,'{user.username}','{user.password}','{user.createtime}')")
        return cursor.rowcount
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)


def getByUserName(username):
    """
    根据用户名查询用户信息
    :param username:
    :return:
    """
    """
        登录判断
        :param user: 
        :return: 
        """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM t_user WHERE username='{username}'")
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)
