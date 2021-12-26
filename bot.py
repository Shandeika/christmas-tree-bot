import configparser
import discord
import requests
import asyncio
import configparser
import math
import os.path

import dis_snek.errors
from dis_snek import Snake, listen, Activity, ActivityType, slash_command, Embed, Intents, InteractionContext, \
    Permissions

config = configparser.ConfigParser()
config.read("config.ini", encoding='utf-8')

bot = Snake(default_prefix=config['Config']['prefix'], intents=Intents.ALL, sync_interactions=True)


def progress(percentage, width=20):
    done = math.floor(width * (percentage / 100))
    return ('█' * done) + ('░' * (width - done))


@listen()
async def on_ready():
    print(f'Bot: {bot.user}')
    await bot.change_presence(activity=Activity(type=ActivityType.PLAYING, name=config['Config']['activity']))




@bot.command(aliases=['помощь'])
async def help(ctx):
    await ctx.message.delete()
    embed=discord.Embed(title="christmas-tree-in-discord", url="https://github.com/Shandeika/christmas-tree-in-discord", description="При входе на сервер проходится по каждому пользователю и добавляет ему 🎄 перед ником и после. Украсит ваш сервер к новому году.")
    embed.set_author(name="Shandy", url="https://vk.com/shandeika", icon_url="https://photo.shandy-dev.ru/shandy/uploads/9de56bb9dc3276a0b7cf678809097521.png")
    embed.set_image(url='https://photo.shandy-dev.ru/shandy/uploads/7cd05c83dae58c59d044fe9e63fb9104.png')
    embed.set_footer(text="Copyright © 2019–2021 Shandy developer agency All Rights Reserved. © 2021")
    await ctx.channel.send(embed=embed)


bot.start(config['Config']['token'])
