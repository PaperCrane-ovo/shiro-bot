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
import keyring


saya = create(Saya)
create(AlconnaBehaviour)

bot = Ariadne(
    connection=config(
        int(keyring.get_password("pgr", "qq")),
        "mashiro",
        HttpClientConfig(host="http://localhost:10250"),
        WebsocketClientConfig(host="http://localhost:10250"),
    )
)

with saya.module_context():
    for module in pkgutil.iter_modules(['modules']):
        saya.require(f'modules.{module.name}')


bot.launch_blocking()
