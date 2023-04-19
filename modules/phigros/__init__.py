'''phigros模块的初始化文件，用于导入模块中的类和函数。'''

import shlex
import os
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
from .song import Song
from .alias import add_alias, get_alias, get_song_list
from .variable import prefix


channel = Channel.current()
channel.name('phigros')
channel.description('phigros相关功能')
channel.author('crane')
Song.read_songs_from_file(os.path.join(
    os.path.dirname(__file__), 'data', 'song.json'))
Song.handle_songs()


__author__ = 'crane'
