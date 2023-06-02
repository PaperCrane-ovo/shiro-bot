'''负责群管理的模块'''
from typing import Annotated
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.entry import MentionMe, GroupMessage, Ariadne, MessageChain, Source, Group, Member, MatchTemplate, Plain, At, MemberPerm, MemberInfo, DetectPrefix


channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage], decorators=[DetectPrefix('我要头衔')]))
async def give_special_title(
        bot: Ariadne,
        group: Group,
        member: Member,
        message: MessageChain,
        source: Source):
    '''自助给予特殊头衔'''

    special_title = message.include(Plain)
    special_title = special_title.display.replace('我要头衔', '').strip()
    if not special_title:
        await bot.send_group_message(group, MessageChain("请在命令后面输入您想要的特殊头衔哦~"), quote=source)
        return

    if group.account_perm != MemberPerm.Owner:
        await bot.send_group_message(group, MessageChain("我不是群主,无法修改头衔哦~"), quote=source)
        return

    await member.modify_info(info=MemberInfo(special_title=special_title))
    await bot.send_group_message(group, MessageChain(f"已将您的特殊头衔修改为{special_title}"), quote=source)

    return
