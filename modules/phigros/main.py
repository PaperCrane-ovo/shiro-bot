'''__init__.py的函数实现.'''
from datetime import datetime
import shlex
from typing import Annotated
import json5
from graia.ariadne.entry import Ariadne, Group, Member, MessageChain, GroupMessage, TempMessage, Source, ForwardNode, Forward, DetectPrefix, Image
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from . import User, Phigros
from .variable import prefix, dir_name


# saya的模块导入只对__init__.py有效,所以在之前的版本中将所有的函数都放在__init__.py中.
# 简化版
# TODO: 重构

channel = Channel.current()
with open(dir_name + '/data/song.json', 'r', encoding='utf-8') as song_file:
    song_info = json5.load(song_file)['song']  # type: ignore

with open(dir_name + '/data/aichan.json', 'r', encoding='utf-8') as ai_chan_file:
    ai_chan_template = json5.load(ai_chan_file)['template']  # type: ignore


@channel.use(ListenerSchema(listening_events=[GroupMessage, TempMessage]))
async def main_phigros(bot: Ariadne,
                       group: Group,
                       member: Member,
                       message: Annotated[MessageChain, DetectPrefix(prefix)],
                       message_type: GroupMessage | TempMessage,
                       source: Source):
    '''
    监听函数,用于处理phigros相关指令

    Parameters:
        bot: Ariadne对象
        group: Group对象
        member: Member对象
        message: MessageChain对象
        message_type: GroupMessage或TempMessage对象
        source: Source对象

    Returns:None
    '''

    # 写了一堆的if-else才发现有更好的匹配器 我是伞兵
    # TODO: 用匹配器重写

    message_str = message.display.strip()
    command, *args = shlex.split(message_str)

    match command:
        case 'bind':
            #  绑定用户信息
            if len(args) == 0:
                if isinstance(message_type, GroupMessage):
                    await bot.send_group_message(group, MessageChain(['请输入session_token!']), quote=source)
                elif isinstance(message_type, TempMessage):
                    await bot.send_temp_message(member, MessageChain(['请输入session_token']), group)
                return
            player = User.get_user(member.id)
            if player is None:
                player = User(member.id, member.name, args[0])
                result = player.register()
                if isinstance(message_type, GroupMessage):
                    await bot.send_group_message(group, MessageChain([result]))
                elif isinstance(message_type, TempMessage):
                    await bot.send_temp_message(member, MessageChain([result]), group)
            else:
                player.session_token = args[0]
                result = player.update_user_info()
                result = '用户信息已存在,'+result
                if isinstance(message_type, GroupMessage):
                    await bot.send_group_message(group, MessageChain([result]))
                elif isinstance(message_type, TempMessage):
                    await bot.send_temp_message(member, MessageChain([result]), group)
        case 'b19':
            # 获取b19数据
            player = User.get_user(member.id)
            if player is None:
                if isinstance(message_type, GroupMessage):
                    await bot.send_group_message(group, MessageChain(['请先绑定session_token!']), quote=source)
                elif isinstance(message_type, TempMessage):
                    await bot.send_temp_message(member, MessageChain(['请先绑定session_token']), group)
                return
            pgr = Phigros(player)

            b19 = await pgr.best19()
            if '--nf' in args:  # not forward
                if isinstance(message_type, GroupMessage):
                    await bot.send_group_message(group, MessageChain([b19]))

            else:
                forward = ForwardNode(
                    target=bot.account,
                    time=datetime.now(),
                    message=MessageChain([b19]),  # type: ignore
                    name='真白鹤甜甜'
                )
                if isinstance(message_type, GroupMessage):
                    return await bot.send_group_message(group, MessageChain(Forward([forward])))

        case 'song':
            # 获取歌曲信息
            pass
            # 需要等到把别名系统写完才能写
        case 'rd':
            # 随机一首歌
            not_forward = False
            use_image = False
            if '--nf' in args:
                args.remove('--nf')
                not_forward = True
            if '--img' in args:
                args.remove('--img')
                use_image = True
            if len(args) == 0 or args[0] == 'aichan':
                ai_template, song = random_song_aichan()
                if use_image:
                    message_chain = MessageChain(
                        [Image(path=dir_name + '/phigros曲绘/' +
                               song['img_path']), ai_template]
                    )
                else:
                    message_chain = MessageChain([ai_template])

                if not not_forward:
                    forward = ForwardNode(
                        target=bot.account,
                        time=datetime.now(),
                        message=message_chain,
                        name='真白鹤甜甜AI酱哒'
                    )
                    message_chain = MessageChain(Forward([forward]))
                if isinstance(message_type, GroupMessage):
                    await bot.send_group_message(group, message_chain)


def random_song_aichan():
    '''随机一首歌'''
    from random import choice
    song = choice(song_info)
    template = choice(ai_chan_template)
    template_str = template.replace(
        r'{歌曲名称}', song['song_name']).replace(r'{作曲家}', song['composer'])
    return template_str, song
