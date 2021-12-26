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

@bot.event
async def on_command_error(ctx, exception): # для команд
#начало Ошибка
    embed=discord.Embed(title=":x: Ошибка!", description=f'{exception}', color=0xff0000)
    embed.set_footer(text="Copyright © 2019–2021 Shandy developer agency All Rights Reserved. © 2021")
#конец
    await ctx.channel.send(embed = embed, delete_after=60)
    print(exception)

async def ny_start(guild):
    #изменение названия сервера
    guild_name_raw = guild.name
    guild_name = guild_name_raw.replace("🎄","")
    try:
        await guild.edit(name=f'🎄{guild_name}🎄')
    except:
        await guild.owner.send('У бота нет прав на изменение названия сервера')
    members = guild.members
    for role_raw in guild.roles:
        #если вы используете своего бота, то тут нужно изменить название роли
        if role_raw.name == 'christmas tree':
            role = role_raw
    #перебор участников и установка ника
    for member in members:
        if member.top_role.position < role.position:
            if member != guild.owner:
                if len(member.display_name) <= 30:
                    raw_name:str = member.display_name
                    name = raw_name.replace("🎄","")
                    await member.edit(nick=f'🎄{name}🎄', reason='Новый год 🎄')
                else:
                    await member.edit(nick='🎄еблан, смени ник🎄', reason='еблан не сменил ник')
                    print('У ', member.name, ' ник больше 32 символов')
            else:
                await guild.owner.send('Хозяину сервера ник менять нельзя :)')
        else:
            print(member.name,'не получит елочку :(')
        await asyncio.sleep(1)
    #назначение прав для канала
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(connect=False),
        guild.owner: discord.PermissionOverwrite(connect=True)
    }
    try:
        await guild.create_voice_channel('Новый год 🎄', overwrites=overwrites, position=0)
    except:
        await guild.owner.send('У бота нет прав на создание каналов')
    return

async def ny_reset(guild):
    #то же самое, но в обратном направлении
    #изменение названия сервера
    guild_name = guild.name
    try:
        await guild.edit(name=guild_name.replace("🎄",""))
    except:
        await guild.owner.send('У бота нет прав на изменение названия сервера')
    members = guild.members
    for role_raw in guild.roles:
        #если вы используете своего бота, то тут нужно изменить название роли
        if role_raw.name == 'christmas tree':
            role = role_raw
    #перебор участников и установка ника
    for member in members:
        if member.top_role.position < role.position:
            if member != guild.owner:
                name:str = member.display_name
                await member.edit(nick=name.replace("🎄",""), reason='Конец нового года')
            else:
                await guild.owner.send('Сбрось ник сам ;)')
        else:
            print(member.name,'не удалось сбросить ник')
        await asyncio.sleep(1)
    #удаление канала "Новый год 🎄"
    for voice in guild.voice_channels:
        if voice.name == 'Новый год 🎄':
            try:
                await voice.delete()
            except:
                await guild.owner.send('У бота нет прав на удаление каналов')

@listen()
async def on_ready():
    print(f'Bot: {bot.user}')
    await bot.change_presence(activity=Activity(type=ActivityType.PLAYING, name=config['Config']['activity']))

@bot.event
async def on_guild_join(guild):
    await guild.owner.send('Привет! :partying_face:')
    embed=discord.Embed(title="Инструкция", url="https://github.com/Shandeika/christmas-tree-in-discord/tree/main#инструкция-по-началу-преображения-сервера", description="Можешь нажать ссылку выше и ты попадешь на репозиторий github с инструкцией", color=0x000000)
    embed.set_author(name="Shandy", url="https://vk.com/shandeika", icon_url="https://photo.shandy-dev.ru/shandy/uploads/9de56bb9dc3276a0b7cf678809097521.png")
    embed.add_field(name="Изменения", value="1. Перед и после ника стоит 🎄\n2. Перед и после названия сервера стоит 🎄", inline=False)
    embed.add_field(name="Если вы готовы, то для начала процесса необходимо ввести", value="`.start`", inline=True)
    embed.add_field(name="Для отмены всех действий нужно ввести", value="`.reset`", inline=True)
    embed.add_field(name="ОЧЕНЬ ВАЖНО!\nРазмести роль бота выше всех!", value="Иначе он не сможет изменять ники", inline=True)
    embed.set_footer(text="Copyright © 2019–2021 Shandy developer agency All Rights Reserved. © 2021")
    await guild.owner.send(embed=embed)



@bot.command(aliases=['помощь'])
async def help(ctx):
    await ctx.message.delete()
    embed=discord.Embed(title="christmas-tree-in-discord", url="https://github.com/Shandeika/christmas-tree-in-discord", description="При входе на сервер проходится по каждому пользователю и добавляет ему 🎄 перед ником и после. Украсит ваш сервер к новому году.")
    embed.set_author(name="Shandy", url="https://vk.com/shandeika", icon_url="https://photo.shandy-dev.ru/shandy/uploads/9de56bb9dc3276a0b7cf678809097521.png")
    embed.set_image(url='https://photo.shandy-dev.ru/shandy/uploads/7cd05c83dae58c59d044fe9e63fb9104.png')
    embed.set_footer(text="Copyright © 2019–2021 Shandy developer agency All Rights Reserved. © 2021")
    await ctx.channel.send(embed=embed)

@bot.command(aliases=['старт'])
@commands.has_guild_permissions(administrator=True)
async def start(ctx):
    await ctx.message.delete()
    await ctx.channel.send('Запущен процесс "новогодизации" сервера, ожидайте, пожалуйста.\nЭтот процесс может длиться достаточно долго.', delete_after=30)
    await ny_start(ctx.guild)
    await ctx.channel.send('Успешно!', delete_after=30)

bot.start(config['Config']['token'])
