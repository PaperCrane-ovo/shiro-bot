'''phigros包bot主模块'''

from os.path import dirname
import json5
import shlex
from typing import Annotated
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.saya import Channel
from graia.ariadne.model import Group, Member
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message import Source
from graia.ariadne.event.message import GroupMessage, TempMessage
from graia.ariadne.message.element import ForwardNode,Forward
from graia.ariadne.app import Ariadne
from graia.ariadne.message.parser.base import DetectPrefix
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

    # 写了一堆的if-else才发现有更好的匹配器 我是伞兵

    message_str = message.display.strip()
    command, *args = shlex.split(message_str)

    match command:
        case 'bind':
            #  绑定用户信息
            if len(args) == 0:
                if isinstance(message_type, GroupMessage):
                    await bot.send_group_message(group, MessageChain([f'请输入session_token!']), quote=source)
                elif isinstance(message_type, TempMessage):
                    await bot.send_temp_message(member, MessageChain([f'请输入session_token']), group)
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

            b19 = pgr.best19()
            if '--nf' in args: # not forward
                if isinstance(message_type, GroupMessage):
                    await bot.send_group_message(group, MessageChain([b19])) # type: ignore

            else:
                forward = ForwardNode(
                    target=bot.account,
                    message=MessageChain([b19]), # type: ignore
                    name = '真白鹤甜甜'
                )
                if isinstance(message_type, GroupMessage):
                    await bot.send_group_message(group, MessageChain(Forward([forward])))




            
        