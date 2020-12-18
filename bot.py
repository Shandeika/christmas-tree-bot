import configparser
import discord
import requests
from discord.ext import commands

config = configparser.ConfigParser()
config.read("config.ini", encoding='utf-8')

bot = commands.Bot(command_prefix=config["Config"]["prefix"], intents=discord.Intents.all())
#удаление стандартной команды help 
bot.remove_command('help')

#class NewYear:

#async def __init__(self, guild):
#    self.guild = guild

async def ny_start(guild):
    #изменение названия сервера
    guild_name_raw = guild.name
    guild_name = guild_name_raw.replace("🎄","")
    await guild.edit(name=f'🎄{guild_name}🎄')
    members = guild.members
    #перебор участников и установка ника
    for member in members:
        if member != guild.owner:
            raw_name:str = member.display_name
            name = raw_name.replace("🎄","")
            await member.edit(nick=f'🎄{name}🎄', reason='Новый год 🎄')
        else:
            await guild.owner.send('Ник установи сам ;)')
    #назначение прав для канала
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(connect=False),
        guild.owner: discord.PermissionOverwrite(connect=True)
    }
    await guild.create_voice_channel('Новый год 🎄', overwrites=overwrites, position=0)
    return

async def ny_reset(guild):
    #то же самое, но в обратном направлении
    #изменение названия сервера
    guild_name = guild.name
    await guild.edit(name=guild_name.replace("🎄",""))
    members = guild.members
    #перебор участников и сброс ника
    for member in members:
        if member != guild.owner:
            name:str = member.display_name
            await member.edit(nick=name.replace("🎄",""), reason='Конец нового года')
        else:
            await guild.owner.send('Сбрось ник сам ;)')
    #удаление канала "Новый год 🎄"
    for voice in guild.voice_channels:
        if voice.name == 'Новый год 🎄':
            await voice.delete()

@bot.event
async def on_ready():
    print("Запустился под", bot.user)
    #установка статуста(Играет в {игра})
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=config["Config"]["activity"]))

@bot.event
async def on_guild_join(guild):
    await guild.owner.send('Привет, я украшу твой сервер! :partying_face:')


@bot.command(aliases=['помощь'])
async def help(ctx):
    await ctx.message.delete()
    embed=discord.Embed(title="christmas-tree-in-discord", url="https://github.com/Shandeika/christmas-tree-in-discord", description="При входе на сервер проходится по каждому пользователю и добавляет ему 🎄 перед ником и после. Украсит ваш сервер к новому году.")
    embed.set_author(name="Shandy", url="https://vk.com/shandeika", icon_url="https://images-ext-1.discordapp.net/external/Nifqk3jVLvmFBCoVz1hauEOemI9X2MJPAGByFf5xpBk/%3Fsize%3D512/https/cdn.discordapp.com/avatars/335464992079872000/9c00b41b1efbc4fd02dce40ff5469bc0.png")
    embed.set_image(url='https://media.discordapp.net/attachments/680742104187797606/789168605961912322/cristmas_tree_bot.png')
    embed.set_footer(text="Copyright © 2019–2020 Shandy developer agency All Rights Reserved. © 2020")
    await ctx.channel.send(embed=embed)

@bot.command(aliases=['старт'])
@commands.has_guild_permissions(administrator=True)
async def start(ctx):
    await ctx.message.delete()
    await ctx.channel.send('Запущен процесс "новогодизации" сервера, ожидайте, пожалуйста.\nЭтот процесс может длиться достаточно долго.', delete_after=30)
    await ny_start(ctx.guild)
    await ctx.channel.send('Успешно!', delete_after=30)

@bot.command(aliases=['сброс'])
@commands.has_guild_permissions(administrator=True)
async def reset(ctx):
    await ctx.message.delete()
    await ctx.channel.send('Запущен процесс сброса изменений, ожидайте, пожалуйста.\nЭтот процесс может длиться достаточно долго.', delete_after=30)
    await ny_reset(ctx.guild)
    await ctx.channel.send('Успешно!', delete_after=30)

bot.run(config["Config"]["token"])
