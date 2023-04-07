'''phigros模块的初始化文件，用于导入模块中的类和函数。'''

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
from .pgrapi import PhigrosUnlimitedAPI
from .score import Phigros
from .user import User
from .main import main_phigros
from .variable import prefix

channel = Channel.current()
channel.name('phigros')
channel.description('phigros相关功能')
channel.author('crane')

# saya监听器只能打在__init__.py里面，所以这里只能写一个监听器，然后把其他的函数放在main.py里面


@channel.use(ListenerSchema(listening_events=[GroupMessage, TempMessage]))
async def phigros(app: Ariadne,
                  group: Group,
                  member: Member,
                  message: Annotated[MessageChain, DetectPrefix(prefix)],
                  message_type: GroupMessage | TempMessage,
                  source: Source):
    '''phigros相关功能'''
    return await main_phigros(app, group, member, message, message_type, source)

__author__ = 'crane'
