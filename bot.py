from discord import Status
from discord.ext import commands

import agent as ag



client = commands.Bot(command_prefix='.')


# Command functions
#region



#endregion



@client.event
async def on_ready():
    print('Bot ready')


@client.command(help='check bot\'s latency')
async def ping(ctxt):
    await ctxt.send(f'{int(client.latency * 1e3)}ms')


@client.command()
async def create(ctxt, id, **kwargs):
    pass



client.run('OTAxODA3MzQ3NTAzMDkxNzYz.YXVPig.KjC0-DDcNDWGZnD3k0VdvjvqQpY')