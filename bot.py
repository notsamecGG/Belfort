from discord.ext import commands, tasks
from discord import utils

from agent import Agent

from dotenv import dotenv_values

from time import asctime


config = dotenv_values(".env")
CHANNEL = config['channel']
BOT_KEY = config['bot_key']
MAINLOOP_TIME = config['mainloop_time']



client = commands.Bot(command_prefix='.')
agents = []


# Functions
#region
def parse_kwargs(args) -> dict:
    kwargs = {}
    
    for arg in args:
        string = str(arg)

        if '=' in string:
            key, value = string.split('=', 1)
            kwargs[key] = value

    return kwargs


async def create_agent(ctxt, id, **kwargs):
    url = ''

    if 'url' in kwargs.keys():
        url = kwargs['url']
        print(url)
        del kwargs['url']
    
    a = Agent(id, url, **kwargs)

    agents.append(a)
    
    await ctxt.send(f'Agent {id} created \n')

    channel = utils.get(client.get_all_channels(), name=CHANNEL)

    await channel.send('@here ------------------------')
    await channel.send(f'>>> {asctime()}, agent: {a.id} snapshot: {len(a.filtered_nft_list[:-1])}')

    for nft in a.filtered_nft_list[:-1]:
        print(nft.data)
        await channel.send(f'```: {nft.data} \n```')


async def delete_agent(ctxt, id):
    for index, agent in enumerate(agents):
        if agent.id == id:
            agents.pop(index)
            
            await ctxt.send(f'Bot {id} removed')
            return


async def update_agents(channel):
    if not agents:
        return

    for agent in agents:
        agent.update()
        changes = agent.compare()

        print(len(changes))
        if len(changes):
            await channel.send('@here ------------------------')
            await channel.send(f'>>> {asctime()}, agent: {agent.id} changes: {len(changes)}')

            for change in changes:
                await channel.send(f'```original: {change[1].data} \n new: {change[1].data}```')


#endregion



# Binding
#region
@client.event
async def on_ready():
    print('Bot ready')

    channel = utils.get(client.get_all_channels(), name=CHANNEL)
    
    print('loop started')
    main_loop.start(channel)


@client.command(help='check bot\'s latency')
async def ping(ctxt):
    await ctxt.send(f'{int(client.latency * 1e3)}ms')


@client.command(help='''create agent "id" -"url" (filters)"name=max_value"''', aliases=['c'])
async def create(ctxt, id, *args,):
    kwargs = parse_kwargs(args)
    await create_agent(ctxt, id, **kwargs)


@client.command(help='''remove agent "id"''', aliases=['r', 'd'])
async def delete(ctxt, id):
    await delete_agent(ctxt, id)
#endregion


@tasks.loop(seconds=int(MAINLOOP_TIME))
async def main_loop(channel):
    await update_agents(channel)
    print('loop done')

client.run(BOT_KEY)