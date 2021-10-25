from discord import Status
from discord.ext import commands
import sys

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    await client.change_presence(status=Status.online)
    print('Bot ready')

@client.command()
async def test_cmd(ctxt):
    await ctxt.send('Hello')

@client.command()
async def ping(ctxt):
    await ctxt.send(f'{int(client.latency * 1e3)}ms')

client.run(API)