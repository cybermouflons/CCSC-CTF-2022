import os
from socket import socket

from pwn import remote
from discord.ext import commands
from decouple import Config, RepositoryEnv


base_dir = os.path.dirname(os.path.realpath(__file__))
env_config = Config(RepositoryEnv(os.path.join(base_dir, ".env")))


BOT_TOKEN = env_config("BOT_TOKEN")
PICKLER_HOST = env_config("PICKLER_HOST", default="pickle-rick")
PICKLER_PORT = env_config("PICKLER_PORT", default=4000, cast=int)

pickle_rick_code = f"""```python
import sys
import pickle
import base64

sys.stdout.write("> ")
sys.stdout.flush()

try:
    pickle_rick = base64.b64decode(sys.stdin.readline().strip())

    if len(pickle_rick) > 23:
        print("That's too much of a pickle")
        exit(1)
    
    print(pickle.loads(pickle_rick))
except Exception as e:
    print(type(e), e)
    print("Flip the pickle over.")
    exit(1)

sys.stdin.close()
```
"""


bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print('Discord bot running as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith("!") and message.guild:
        await message.channel.send("Pickle Rick only available in private message!")
    else:
        await bot.process_commands(message)

@bot.command(help="Show Pickle Rick's code")
async def code(ctx):
    await ctx.channel.send(pickle_rick_code)

@bot.command(help="Transform a pickle back to normal form!")
async def unpickle(ctx, pickle: str):
    try:
        r = remote(PICKLER_HOST, PICKLER_PORT)
        r.recvuntil(b"> ")
        r.sendline(pickle.encode())
        await ctx.channel.send(r.recvall())
    except Exception as e:
        await ctx.channel.send("Something is wrong...")

bot.run(BOT_TOKEN)