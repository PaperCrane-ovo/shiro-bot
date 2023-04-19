'''别名系统'''
import os
from typing import Annotated
from datetime import datetime
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.entry import Ariadne, Group, Member, MessageChain, GroupMessage, FriendMessage, Source, ForwardNode, Forward, DetectPrefix, Image, Friend
from .song import Song


channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def add_alias(bot: Ariadne,
                    message: Annotated[MessageChain, DetectPrefix('添加别名')],
                    group: Group,
                    source: Source):
    '''临时开启添加别名函数,供社区自行添加,暂时不审核.'''
    args = message.display.split()
    if len(args) == 0 or args[0] == 'help':
        help_text = '''添加别名帮助:
        添加别名 help: 显示本帮助
        添加别名 list: 显示所有歌曲列表
        添加别名 歌曲编号 [别名1] [别名2] ...
        例如: 添加别名 60 烤全压 烤全鸭 烤全押
        可以为Burn(编号为60,可以用list查看歌曲编号)添加别名为烤全压,烤全鸭,烤全押
        请保证别名中尽量不要有空格
        '''
        await bot.send_group_message(group, MessageChain(help_text), quote=source)

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
        await bot.send_group_message(group, MessageChain([Forward([forward_node])]), quote=source)

        return

    song_number = int(args[0])
    alias = args[1:]
    song = Song.instances_list[song_number-1]

    for i in alias:
        if i in song.alias:
            await bot.send_group_message(group, MessageChain(f'别名{i}已存在,请勿重复添加'), quote=source)
            return

    song.alias += alias
    Song.dump2json(os.path.join(
        os.path.dirname(__file__), 'data', 'song.json'))
    await bot.send_group_message(group, MessageChain(f'添加别名成功,当前别名有\n{song.alias}'), quote=source)

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
        查别名 help: 显示本帮助
        查别名 歌曲编号
        例如: 查别名 60
        可以查看Burn(编号为60,可以用list查看歌曲编号)的别名
        编号可以输入歌曲列表来查看.
        查别名 歌曲名 (施工中)
        例如: 查别名 Burn 
        可以查看Burn的别名
        '''
        await bot.send_group_message(group, MessageChain(help_text), quote=source)
        return
    song_number = int(args[0])
    song = Song.instances_list[song_number-1]
    await bot.send_group_message(group, MessageChain(f'当前别名有{song.alias}'), quote=source)
    return
