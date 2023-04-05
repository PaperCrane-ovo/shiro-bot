'''phigros包bot主模块'''

from os.path import dirname
import json5
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.saya import Channel
from graia.ariadne.model import Group
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import GroupMessage
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


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def phigros(bot: Ariadne, group: Group, message: MessageChain):
    '''
    监听函数,用于处理phigros相关指令

    Parameters:
        bot: Ariadne对象
        group: Group对象
        message: MessageChain对象

    Returns:None
    '''
    