'''bot主文件'''
import pkgutil
from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
    config,
)
from graia.saya import Saya
from arclet.alconna.graia.saya import AlconnaBehaviour, AlconnaSchema
from arclet.alconna.graia import Match, AlconnaDispatcher
from arclet.alconna import Alconna
from pathlib import Path
import json5


saya = create(Saya)
create(AlconnaBehaviour)
with open(Path(__file__).parent / 'account.json', 'r', encoding='utf-8') as f:
    account = json5.load(f)

qq = account['qq']
verify_key = account['verify_key']
port = account['port']


bot = Ariadne(
    connection=config(
        qq,
        verify_key,
        HttpClientConfig(host=f"http://localhost:{port}"),
        WebsocketClientConfig(host=f"http://localhost:{port}"),
    )
)

with saya.module_context():
    for module in pkgutil.iter_modules(['modules']):
        saya.require(f'modules.{module.name}')


bot.launch_blocking()
