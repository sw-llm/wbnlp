"""
    用户实体类
    作者 : 小锋老师
    官网 : www.python222.com
"""


# 用户实体类
class User:
    # 编号 主键ID
    id = None
    # 用户名
    username = None
    # 密码
    password = None
    # 注册日期
    createtime = None

    def __init__(self, username, password):
        self.username = username
        self.password = password
