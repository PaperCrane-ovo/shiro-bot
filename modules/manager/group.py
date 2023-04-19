'''负责群管理的模块'''
from typing import Annotated
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.entry import MentionMe, GroupMessage, Ariadne, MessageChain, Source, Group, Member, MatchTemplate, Plain


channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def give_special_title(
        bot: Ariadne,
        group: Group,
        member: Member,
        message: Annotated[MessageChain, MatchTemplate([MentionMe(), Plain("我要头衔")])],
        source: Source):
    '''自助给予特殊头衔'''
    special_title = message.display.strip()
    # 缺一点异常处理
    await member.modify_info(special_title=special_title)
    await bot.send_group_message(group, MessageChain(f"已将您的特殊头衔修改为{special_title}"), quote=source)
    return
