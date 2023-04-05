'''phigros 用户类,包含用户昵称,session-token'''

import json5
from .pgrapi import PhigrosUnlimitedAPI


class User:
    '''
    phigros 用户类

    包含用户昵称,qq,session-token,rks
    '''
    file_path = __file__.replace("user.py", "users.json")

    def __init__(self, qq: int, username: str, session_token: str):
        '''
        初始化用户类

        Parameters:
            qq: 用户qq号
            username: 用户昵称
            session_token: 用户session-token

        '''
        self.username = username
        self.qq = str(qq)
        self.session_token = session_token
        self.rks = 0.0

    def dump2json(self):
        '''
        将用户信息转换为以qq为索引的json格式

        return: json格式的用户信息

        '''
        return json5.dumps({self.qq: {"username": self.username, "token": self.session_token, "rks": self.rks}})

    def loadfromjson(self, jsonstr: str):
        '''
        从json格式的用户信息中读取用户信息

        Parameters:
            jsonstr: json格式的用户信息


        '''
        return json5.loads(jsonstr)

    def register(self):
        '''
        将用户信息写入json文件

        '''
        try:
            with open(User.file_path, "r", encoding="utf-8") as f:
                user_dict = json5.loads(f.read())
        except FileNotFoundError:
            return '文件未找到,请联系管理员'

        user_dict[self.qq] = {"username": self.username,                    # type: ignore
                              "token": self.session_token, "rks": self.rks}

        with open(User.file_path, "w", encoding="utf-8") as f:
            f.write(json5.dumps(user_dict))

        return '注册成功,请查询一次b19数据以检测session_token是否正确'

    def update_rks(self, rks):
        '''
        更新用户rks

        Parameters:
            rks: 用户rks

        '''
        self.rks = rks

    def update_user_info(self):
        '''
        更新用户信息

        '''
        try:
            with open(User.file_path, "r", encoding="utf-8") as f:
                user_dict = json5.loads(f.read())
        except FileNotFoundError:
            return '文件未找到,请联系管理员'

        assert isinstance(user_dict, dict)
        user_dict[self.qq]["rks"] = self.rks
        user_dict[self.qq]["username"] = self.username

        with open(User.file_path, "w", encoding="utf-8") as f:
            f.write(json5.dumps(user_dict))

        return '更新成功'

    def get_user(self, qq: int):
        '''
        从json文件中获取用户信息

        Parameters:
            qq: 用户qq号

        Returns:
            用户信息|错误信息

        '''
        try:
            with open(User.file_path, "r", encoding="utf-8") as f:
                user_dict = json5.loads(f.read())
        except FileNotFoundError:
            return None

        assert isinstance(user_dict, dict)
        if str(qq) in user_dict:
            return user_dict[str(qq)]
        return None
