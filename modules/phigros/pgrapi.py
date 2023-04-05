'''PhigrosUnlimitedAPI主模块'''

import aiohttp
from keyring import get_password


class PhigrosUnlimitedAPI:
    '''
    PhigrosUnlimitedAPI主类

    Parameters:
        api_url: PhigrosUnlimitedAPI的url
        api_token: PhigrosUnlimitedAPI的token
        headers: 请求头
    '''

    def __init__(self) -> None:
        '''初始化PhigrosUnlimitedAPI主类'''
        self.api_url = str(get_password('pgr', 'api_url'))
        self.api_token = str(get_password('pgr', 'api_token'))
        self.headers = {"Authorization": f"Bearer {self.api_token}"}

    async def user_best19(self, session_token: str, overflow: int = 0, withsonginfo: bool = False):
        '''
        获取用户b19数据

        :param SessionToken: 用户session-token
        :param overflow: 0:不显示溢出数据,溢出数据作为推分指导
        :param withsonginfo: 是否显示歌曲信息

        :return: 用户b19数据|错误信息
        '''
        url = self.api_url + \
            f"user/best19?SessionToken={session_token}&overflow={overflow}&withsonginfo={withsonginfo}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url=url, headers=self.headers)as reqs:
                    return await reqs.json()
        except Exception as error:
            return f'Error {type(error)}'

    async def user_best(self, session_token: str, songid: str, level: str = "IN", withsonginfo: bool = False):
        '''
        获取单曲最高成绩

        Parameters:
            session_token: 用户session-token
            songid: 歌曲id
            level: 难度
            withsonginfo: 是否显示歌曲信息

        Returns:
            单曲最高成绩|错误信息
        '''
        url = self.api_url + \
            f"user/best?SessionToken={session_token}&songid={songid}&level={level}&withsonginfo={withsonginfo}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url=url, headers=self.headers)as reqs:
                    return await reqs.json()
        except Exception as error:
            return f'Error {type(error)}'

    async def song_info(self, songid: str):
        '''
        获取歌曲信息

        Parameters:
            songid: 歌曲id

        Returns:
            歌曲信息|错误信息
        '''
        url = self.api_url + f"song/info?songid={songid}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url=url)as reqs:
                    return await reqs.json()
        except Exception as error:
            return f'Error {type(error)}'

    async def song_random(self):
        '''
        随机歌曲

        Returns: 随机歌曲|错误信息
        '''
        url = self.api_url + r"song/random"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url)as reqs:
                    return await reqs.json()
        except Exception as error:
            return f'Error {type(error)}'
