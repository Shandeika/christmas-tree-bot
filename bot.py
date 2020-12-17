import configparser
import discord
from discord.ext import commands

config = configparser.ConfigParser()
config.read("config.ini")

bot = commands.Bot(command_prefix=config["prefix"], intents=discord.Intents.all())
#удаление стандартной команды help 
bot.remove_command('help')

@bot.event
async def on_ready():
    print("Запустился под", bot.user)
    #установка статуста(Играет в {игра})
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=config["activity"]))

@bot.event
async def on_guild_join(guild):
    #изменение названия сервера
    guild_name = guild.name
    await guild.edit(name=f'🎄{guild_name}🎄')
    members = guild.members
    #перебор участников и выдача роли
    for member in members:
        name = member.name
        await member.edit(name=f'🎄{name}🎄', reason='Новый год 🎄')
    #назначение прав для канала
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(connect=False),
        guild.owner: discord.PermissionOverwrite(connect=True)
    }
    await guild.create_voice_channel('Новый год 🎄', overwrites=overwrites)

@bot.command(aliases=['помощь'])
async def help(ctx):
    embed=discord.Embed(title="christmas-tree-in-discord", url="https://github.com/Shandeika/christmas-tree-in-discord", description="При входе на сервер проходится по каждому пользователю и добавляет ему 🎄 перед ником и после. Украсит ваш сервер к новому году.")
    embed.set_author(name="Shandy", url="https://vk.com/shandeika", icon_url="https://images-ext-1.discordapp.net/external/Nifqk3jVLvmFBCoVz1hauEOemI9X2MJPAGByFf5xpBk/%3Fsize%3D512/https/cdn.discordapp.com/avatars/335464992079872000/9c00b41b1efbc4fd02dce40ff5469bc0.png")
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/680742104187797606/789168605961912322/cristmas_tree_bot.png')
    embed.set_footer(text="Copyright © 2019–2020 Shandy developer agency All Rights Reserved. © 2020")
    await ctx.channel.send(embed=embed)

bot.run(config["token"])