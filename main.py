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


saya = create(Saya)

bot = Ariadne(
    connection=config(
        1284086758,
        "mashiro",
        HttpClientConfig(host="http://localhost:10250"),
        WebsocketClientConfig(host="http://localhost:10250"),
    )
)

with saya.module_context():
    for module in pkgutil.iter_modules(['modules']):
        saya.require(f'modules.{module.name}')

bot.launch_blocking()
