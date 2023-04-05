'''phigros包bot主模块'''

from os.path import dirname
import shlex
import json5
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.saya import Channel
from graia.ariadne.model import Group, Member
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message import Source
from graia.ariadne.event.message import GroupMessage, TempMessage
from graia.ariadne.app import Ariadne
from .user import User
from .score import Phigros


channel = Channel.current()

dir_name = dirname(__file__)
with open(f'{dir_name}/config.json', 'r', encoding='utf-8') as f:
    config = json5.load(f)
pgr_prefix = config['pgr_prefix']  # type: ignore
with open(f'{dir_name}/../../config.json', 'r', encoding='utf-8') as f:
    config = json5.load(f)
bot_prefix = config['instr_prefix']  # type: ignore


@channel.use(ListenerSchema(listening_events=[GroupMessage, TempMessage]))
async def phigros(bot: Ariadne,
                  group: Group,
                  member: Member,
                  message: MessageChain,
                  message_type: GroupMessage | TempMessage,
                  source: Source):
    '''
    监听函数,用于处理phigros相关指令

    Parameters:
        bot: Ariadne对象
        group: Group对象
        message: MessageChain对象

    Returns:None
    '''
    is_pgr_command = False
    prefix, command, *args = shlex.split(message.display)

    if (isinstance(pgr_prefix, str) and prefix == pgr_prefix) or (isinstance(pgr_prefix, list) and prefix in pgr_prefix):
        is_pgr_command = True

    elif prefix == bot_prefix:
        if (isinstance(pgr_prefix, str) and command == pgr_prefix) or (isinstance(pgr_prefix, list) and command in pgr_prefix):
            is_pgr_command = True
            command = args[0]
            args = args[1:]
    elif bot_prefix in prefix:
        prefix = prefix.strip(bot_prefix)
        if (isinstance(pgr_prefix, str) and prefix == pgr_prefix) or (isinstance(pgr_prefix, list) and prefix in pgr_prefix):
            is_pgr_command = True

    if is_pgr_command:
        user = User.get_user(member.id)
        if user is None:
            if isinstance(message_type, GroupMessage):
                await bot.send_group_message(group, MessageChain([f'请先注册,指令为{pgr_prefix[-1]}register']), quote=source)
            elif isinstance(message_type, TempMessage):
                await bot.send_temp_message(member, MessageChain([f'请先注册,指令为{pgr_prefix[-1]}register']), group)
            return
        