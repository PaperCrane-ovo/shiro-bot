'''phigros模块的初始化文件，用于导入模块中的类和函数。'''

from os.path import dirname
import shlex
from typing import Annotated
from datetime import datetime
import json5
from graia.ariadne.message.parser.base import DetectPrefix
from graia.ariadne.app import Ariadne
from graia.ariadne.message.element import ForwardNode, Forward
from graia.ariadne.event.message import GroupMessage, TempMessage
from graia.ariadne.message import Source
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from .pgrapi import PhigrosUnlimitedAPI as PhigrosUnlimitedAPI
from .score import Phigros as Phigros
from .user import User as User
from .main import main_phigros as main_phigros
dir_name = dirname(__file__)


channel = Channel.current()


with open(f'{dir_name}/config.json', 'r', encoding='utf-8') as f:
    config = json5.load(f)
pgr_prefix = config['pgr_prefix']  # type: ignore
with open(f'{dir_name}/../../config.json', 'r', encoding='utf-8') as f:
    config = json5.load(f)
bot_prefix = config['instr_prefix']  # type: ignore

prefix = [bot_prefix+pgr_prefix] if isinstance(pgr_prefix, str) else [
    bot_prefix+p for p in pgr_prefix]
prefix += pgr_prefix if isinstance(pgr_prefix, list) else [pgr_prefix]
prefix += [bot_prefix + ' '+p for p in pgr_prefix] if isinstance(
    pgr_prefix, list) else [bot_prefix+' '+pgr_prefix]
prefix = list(set(prefix))


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, TempMessage],
    )
)
async def phigros(bot: Ariadne,
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
    return await main_phigros(bot, group, member, message, message_type, source)


__author__ = 'crane'
