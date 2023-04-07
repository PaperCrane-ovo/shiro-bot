'''__init__.py的函数实现.'''
from datetime import datetime
import shlex
from typing import Annotated
import json5
from graia.ariadne.entry import Ariadne, Group, Member, MessageChain, GroupMessage, TempMessage, Source, ForwardNode, Forward, DetectPrefix
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from . import User, Phigros
from .variable import prefix, dir_name, game_info


# saya的模块导入只对__init__.py有效,所以在之前的版本中将所有的函数都放在__init__.py中.
# 简化版

channel = Channel.current()

with open(f'{dir_name}/GameInformation.json', 'r', encoding='utf-8') as f:
    GameInformation = json5.load(f)


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
                    await bot.send_group_message(group, MessageChain(Forward([forward])))

        case 'song':
            # 获取歌曲信息
            pass
