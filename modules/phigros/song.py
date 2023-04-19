'''phigros 歌曲类'''
import json5
import os
from datetime import datetime
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.entry import Ariadne, Group, Member, MessageChain, GroupMessage, FriendMessage, Source, ForwardNode, Forward, DetectPrefix, Image, Friend
from typing import Annotated

channel = Channel.current()


class Song:
    '''歌曲类,包含歌曲的所有信息以及难度谱师等等.'''

    song_info: list[dict]
    instances: dict = {}
    song_list: list = [str]

    @classmethod
    def read_songs_from_file(cls, file_path: str):
        '''从文件中读取歌曲信息'''
        with open(file_path, 'r', encoding='utf-8') as f:
            cls.song_info = json5.load(f)['songs']  # type: ignore
        cls.song_list = [
            f"{song['song_number']}.{song['song_name']} ({song['composer']})" for song in cls.song_info]

    @classmethod
    def handle_songs(cls):
        '''处理歌曲信息'''
        cnt = 1
        for song in cls.song_info:
            cls(song['song_number'], song['song_id'], song['song_name'], song['difficulty'],
                song['level'], song['composer'], song['illustrator'], song['chapter'])

    def __init__(self,
                 song_number,
                 song_id,
                 song_name,
                 difficulty,
                 level,
                 composer,
                 illustrator,
                 charter,
                 alias: list[str] = []):
        '''初始化歌曲类'''
        self.song_number = song_number
        self.song_id = song_id
        self.song_name = song_name
        self.difficulty = difficulty
        self.level = level
        self.composer = composer
        self.illustrator = illustrator
        self.charter = charter
        self.alias = alias
        self.img_path = f'{str(song_number)+"_"+song_name.replace(" ", "")}.png'
        Song.instances[song_id] = self

    def __str__(self):
        '''返回歌曲信息'''

    @classmethod
    def dump2json(cls, file_path):
        '''将所有实例转换为json'''
        song_dict = {'songs': []}
        for _, song in cls.instances.items():
            song_dict['songs'].append(song.__dict__)
        with open(file_path, 'w', encoding='utf-8') as f:
            json5.dump(song_dict, f, indent=4, ensure_ascii=False)


@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage]))
async def add_alias(bot: Ariadne,
                    message: Annotated[MessageChain, DetectPrefix('添加别名')],
                    group: Group,
                    friend: Friend,
                    source: Source,
                    message_type: GroupMessage | FriendMessage):
    '''临时开启添加别名函数,供社区自行添加,暂时不审核.'''
    args = message.display.split()
    if len(args) == 0 or args[0] == 'help':
        help_text = '''添加别名帮助:
        添加别名 help: 显示本帮助\n
        添加别名 list: 显示所有歌曲列表\n
        添加别名 歌曲编号 [别名1] [别名2] ...\n
        例如: 添加别名 60 烤全压 烤全鸭 烤全押\n
        可以为Burn(编号为60,可以用list查看歌曲编号)添加别名为烤全压,烤全鸭,烤全押\n
        请保证别名中尽量不要有空格\n
        '''
        if isinstance(message_type, GroupMessage):
            await bot.send_group_message(group, MessageChain(help_text), quote=source)
        elif isinstance(message_type, FriendMessage):
            await bot.send_friend_message(friend, MessageChain(help_text))
        return
    if args[0] == 'list':
        song_list = Song.song_list
        song_list_text = '歌曲列表:\n'
        for song in song_list:
            song_list_text += song+'\n'
        forward_node = ForwardNode(
            target=bot.account,
            time=datetime.now(),
            message=MessageChain(song_list_text),
            name='真白bot'
        )
        if isinstance(message_type, GroupMessage):
            await bot.send_group_message(group, MessageChain([Forward([forward_node])]), quote=source)
        elif isinstance(message_type, FriendMessage):
            await bot.send_friend_message(friend, MessageChain([Forward([forward_node])]))
        return

    song_number = int(args[0])
    alias = args[1:]
    song = Song.instances[song_number-1]
    song.alias += alias
    Song.dump2json(os.path.join(
        os.path.dirname(__file__), 'data', 'song.json'))
    if isinstance(message_type, GroupMessage):
        await bot.send_group_message(group, MessageChain(f'添加别名成功,当前别名有{song.alias}'), quote=source)
    elif isinstance(message_type, FriendMessage):
        await bot.send_friend_message(friend, MessageChain(f'添加别名成功,当前别名有{song.alias}'))
    return


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def get_song_list(bot: Ariadne,
                        message: Annotated[MessageChain, DetectPrefix('歌曲列表')],
                        group: Group,
                        source: Source):
    '''获取歌曲列表'''
    song_list = Song.song_list
    song_list_text = '歌曲列表:\n'
    for song in song_list:
        song_list_text += song+'\n'
    forward_node = ForwardNode(
        target=bot.account,
        time=datetime.now(),
        message=MessageChain(song_list_text),
        name='真白bot'
    )
    await bot.send_group_message(group, MessageChain([Forward([forward_node])]), quote=source)
    return


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def get_alias(bot: Ariadne,
                    message: Annotated[MessageChain, DetectPrefix('查别名')],
                    group: Group,
                    source: Source):
    '''获取别名'''
    args = message.display.split()
    if len(args) == 0 or args[0] == 'help':
        help_text = '''查别名帮助:
        查别名 help: 显示本帮助\n
        查别名 歌曲编号\n
        例如: 查别名 60\n
        可以查看Burn(编号为60,可以用list查看歌曲编号)的别名\n
        编号可以输入歌曲列表来查看.\n
        查别名 歌曲名 (施工中)\n
        例如: 查别名 Burn \n
        可以查看Burn的别名\n
        '''
        await bot.send_group_message(group, MessageChain(help_text), quote=source)
        return
    song_number = int(args[0])
    song = Song.instances[song_number-1]
    await bot.send_group_message(group, MessageChain(f'当前别名有{song.alias}'), quote=source)
    return

if __name__ == '__main__':
    Song.read_songs_from_file(os.path.join(
        os.path.dirname(__file__), 'data', 'song.json'))
    print(Song.song_list)
