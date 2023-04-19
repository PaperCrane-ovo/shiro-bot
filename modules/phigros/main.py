'''__init__.py的函数实现.'''
from datetime import datetime
import shlex
from typing import Annotated
import json5
from graia.ariadne.entry import Ariadne, Group, Member, MessageChain, GroupMessage, TempMessage, Source, ForwardNode, Forward, DetectPrefix, Image, Plain
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from . import User, Phigros
from .variable import prefix, dir_name
from .song import Song

# saya的模块导入只对__init__.py有效,所以在之前的版本中将所有的函数都放在__init__.py中.
# 简化版
# TODO: 重构

channel = Channel.current()
with open(dir_name + '/data/song.json', 'r', encoding='utf-8') as song_file:
    song_info = json5.load(song_file)['songs']  # type: ignore

with open(dir_name + '/data/aichan.json', 'r', encoding='utf-8') as ai_chan_file:
    ai_chan_template = json5.load(ai_chan_file)['template']  # type: ignore


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def main_phigros(bot: Ariadne,
                       group: Group,
                       member: Member,
                       message: Annotated[MessageChain, DetectPrefix(prefix)],
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
            await bot.send_group_message(group, MessageChain(['为防止隐私泄露,请私聊我使用//bind <session_token>绑定session_token']), quote=source)
        case 'b19':
            # 获取b19数据
            player = User.get_user(member.id)
            if player is None:
                await bot.send_group_message(group, MessageChain(['请先私聊用//bind绑定session_token!']), quote=source)
                return
            pgr = Phigros(player)

            b19 = await pgr.best19()
            if '--nf' in args:  # not forward
                await bot.send_group_message(group, MessageChain([b19]))

            else:
                forward = ForwardNode(
                    target=bot.account,
                    time=datetime.now(),
                    message=MessageChain([b19]),  # type: ignore
                    name='真白鹤甜甜'
                )
                return await bot.send_group_message(group, MessageChain(Forward([forward])))

        case 'song':
            if len(args) == 1 and args[0].isdigit():
                song_number = int(args[0])
                if song_number > len(song_info):
                    await bot.send_group_message(group, MessageChain(['没有这首歌哦']))
                    return
                result = Song.search_song_by_number(song_number)
            else:
                song_name = ''.join(args)
                result = Song.search_song_by_alias(song_name)
            if isinstance(result, list):
                await bot.send_group_message(group, MessageChain(Plain('为您找到了以下可能的答案:\n'+'\n'.join(result))))
            else:
                await bot.send_group_message(group, MessageChain(Plain(result)))
            return

        case 'best':
            # 获取最佳成绩
            player = User.get_user(member.id)
            if player is None:
                await bot.send_group_message(group, MessageChain(['请先私聊用//bind绑定session_token!']), quote=source)
                return
            pgr = Phigros(player)
            level = 'IN'
            result = Song.search_song_by_alias(args[0])

            if not result or isinstance(result, list):
                await bot.send_group_message(group, MessageChain(['没有找到这首歌哦']))
                return
            if len(args) == 1 and result.difficulty[3] != 0.0:
                level = 'AT'
            elif len(args) == 2:
                level = args[1].upper()

            best = await pgr.single_best(result.song_id, level)
            return await bot.send_group_message(group, MessageChain([best]), quote=source)

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
                await bot.send_group_message(group, message_chain)


def random_song_aichan():
    '''随机一首歌'''
    from random import choice
    song = choice(song_info)
    template = choice(ai_chan_template)
    template_str = template.replace(
        r'{歌曲名称}', song['song_name']).replace(r'{作曲家}', song['composer'])
    return template_str, song


@channel.use(ListenerSchema(listening_events=[TempMessage]))
async def bind_session_token(
    bot: Ariadne,
    member: Member,
    group: Group,
    message: Annotated[MessageChain, DetectPrefix('//bind')],
):
    '''绑定session_token'''
    session_token = message.display.strip()
    if session_token == '':
        await bot.send_temp_message(member, MessageChain(['请输入session_token']), group)
        return
    player = User.get_user(member.id)
    if player is None:
        player = User(member.id, member.name, session_token)
        result = player.register()
        await bot.send_temp_message(member, MessageChain([result]), group)
    else:
        player.session_token = session_token
        result = player.update_user_info()
        result = '用户信息已存在,'+result
        await bot.send_temp_message(member, MessageChain([result]), group)
