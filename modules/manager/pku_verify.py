'''pku邮件验证入群模块'''
import os
import json5
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.entry import MentionMe, GroupMessage, Ariadne, MessageChain, Source, Group, Member, MatchTemplate, Plain, At, MemberPerm, MemberInfo, MemberJoinRequestEvent

channel = Channel.current()


class GroupVerified:
    '''需要验证入群的类'''
    instances = {}

    @classmethod
    def load(cls, filepath: str):
        '''从配置文件加载验证信息'''
        with open(filepath, 'r', encoding='utf-8') as file:
            groups = json5.load(file)  # type: dict
        for group in groups.items():
            # TODO
            pass

    def __init__(self, group_id: int, regex_str: str = r''):
        '''
        通过 group_id 构造一个群组,包括群号和已入群通过申请的qq号,以及邮箱验证规则.

        Parameters:
        ---
        group_id:int
            需要验证的群号

        Returns:
        -------
        None
        '''
        self.group_id = group_id
        self.already_passed_qq = []
        self.regex_str = regex_str


@channel.use(ListenerSchema(listening_events=[MemberJoinRequestEvent]))
async def member_join_pku_group(
    event: MemberJoinRequestEvent,
    bot: Ariadne
):
    '''有新成员申请进入pku群'''
    group = event.source_group
    inviter = event.inviter_id
    joiner = event.supplicant
