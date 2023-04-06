'''Phigros模块的score子模块,用于调用api并返回可读数据.'''

from .pgrapi import PhigrosUnlimitedAPI
from .user import User


class Phigros:  # [too-few-public-methods]
    '''
    使用PhigrosUnlimitedAPI获取数据
    并可以提供歌曲定数等方法的类.

    '''

    def __init__(self, user: User):
        '''
        初始化Phigros类

        Parameters:
            user: 用户类

        '''
        self.api = PhigrosUnlimitedAPI()
        self.user = user

    async def best19(self, overflow: int = 0) -> str:
        '''
        获取用户b19数据

        Parameters:
            overflow: 0:不显示溢出数据,溢出数据作为推分指导

        Returns: 用户b19数据

        '''
        response = await self.api.user_best19(self.user.session_token, overflow)
        if isinstance(response, str) and response.startswith('Error'):
            return '获取数据失败,请稍后再试'

        assert isinstance(response, dict)
        if response['status'] == 0:
            return '数据解码失败,请稍后再试'

        content = response['content']

        challenge_mode = {"1": "绿", "2": "蓝", "3": "红", "4": "金", "5": "彩"}
        challenge_score = str(content['ChallengeModeRank'])

        return_value = f"玩家:{content['PlayerID']}的游戏数据如下:\n\n"
        return_value += f"RankingScore:{content['RankingScore']}\n"
        return_value += f"课题模式成绩:{challenge_mode[challenge_score[0]]}{challenge_score[1:]}\n\n"
        # 更新玩家信息
        self.user.username = content['PlayerID']
        self.user.rks = content['RankingScore']
        self.user.update_user_info()

        best_list = content['best_list']['best']  # type: list
        if content['best_list']['phi']:
            return_value += f"最高收歌为:{best_list[0]['songname']}({best_list[0]['level']}),定数{best_list[0]['rating']}\n\n"
            best_list = best_list[1:]
        return_value += "b19数据如下:\n\n"
        count = 1
        for best in best_list:
            return_value += f"{count}. {best['songname']}({best['level']}),定数:{best['rating']},acc:{best['acc']},单曲rks:{best['rks']}\n"
            count += 1

        return return_value

    async def single_best(self, songid: str, level: str = "IN", withsonginfo: bool = False):
        '''
        获取用户单曲best数据

        Parameters:
            songid: 歌曲id
            level: 难度
            withsonginfo: 是否返回歌曲信息

        Returns: 用户单曲best数据

        '''
        return await self.api.user_best(self.user.session_token, songid, level, withsonginfo)
