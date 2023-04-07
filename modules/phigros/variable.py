'''一些预处理的变量'''
from os.path import dirname
import json5

# 当前文件夹的路径
dir_name = dirname(__file__)

# phigros命令前缀
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

# 歌曲信息 虽然很大 但不是很大
with open(f'{dir_name}/GameInformation.json', 'r', encoding='utf-8') as f:
    game_info = json5.load(f)['song']  # type: ignore
