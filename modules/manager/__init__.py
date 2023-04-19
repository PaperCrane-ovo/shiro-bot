'''shiro bot管理模块,负责对bot的底层管理.'''
from os.path import dirname
from typing import Annotated
from graia.ariadne.entry import *
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
import json5
channel = Channel.current()
saya = Saya.current()

dir_name = dirname(__file__)
with open(f'{dir_name}/../../config.json', 'r', encoding='utf-8') as f:
    config = json5.load(f)
bot_prefix = config['instr_prefix']  # type: ignore

channel.name('manager')
channel.description('shiro bot管理模块,负责对bot的底层管理.')
channel.author('crane')


@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage],
    )
)
async def reload_modules(bot: Ariadne,
                         friend: Friend,
                         message_chain: Annotated[MessageChain, DetectPrefix(bot_prefix+'重载模组')],
                         source: Source):
    '''
    重载模块

    Parameters:
        bot: Ariadne对象
        friend: Friend对象
        message: MessageChain对象
        source: Source对象

    Returns:None
    '''
    with open(f'{dir_name}/admins.json', 'r', encoding='utf-8') as f:
        admins = json5.load(f)['superadmin']  # type: ignore
    if friend.id not in admins:
        return await bot.send_friend_message(friend, MessageChain("您没有权限执行此操作,只有超级管理员可以哦"), quote=source)
    channel_path = str(message_chain)
    channel_path = 'modules.'+channel_path

    if not (_channel := saya.channels.get(channel_path)):
        return await bot.send_friend_message(friend, MessageChain("该模组未安装, 您可能需要安装它"), quote=source)
    try:
        saya.reload_channel(_channel)
    except Exception:
        await bot.send_friend_message(friend, MessageChain(f"重载 {channel_path} 失败！"), quote=source)
    else:
        return await bot.send_friend_message(friend, MessageChain(f"重载 {channel_path} 成功"), quote=source)
