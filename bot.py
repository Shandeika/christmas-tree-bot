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

@bot.event
async def on_command_error(ctx, exception): # для команд
#начало Ошибка
    embed=discord.Embed(title=":x: Ошибка!", description=f'{exception}', color=0xff0000)
    embed.set_footer(text="Copyright © 2019–2020 Shandy developer agency All Rights Reserved. © 2020")
#конец
    await ctx.channel.send(embed = embed, delete_after=60)
    print(exception)

async def ny_start(guild):
    #изменение названия сервера
    guild_name_raw = guild.name
    guild_name = guild_name_raw.replace("🎄","")
    await guild.edit(name=f'🎄{guild_name}🎄')
    members = guild.members
    for role_raw in guild.roles:
        #если вы используете своего бота, то тут нужно изменить название роли
        if role_raw.name == 'christmas tree':
            role = role_raw
    #перебор участников и установка ника
    for member in members:
        if member.top_role.position < role.position:
            if member != guild.owner:
                raw_name:str = member.display_name
                name = raw_name.replace("🎄","")
                await member.edit(nick=f'🎄{name}🎄', reason='Новый год 🎄')
            else:
                await guild.owner.send('Ник установи сам ;)')
        else:
            print(member.name,'не получит елочку :(')
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
    await guild.owner.send('Привет! :partying_face:')
    embed=discord.Embed(title="Инструкция", url="https://github.com/Shandeika/christmas-tree-in-discord/tree/main#инструкция-по-началу-преображения-сервера", description="Можешь нажать ссылку выше и ты попадешь на репозиторий github с инструкцией", color=0x000000)
    embed.set_author(name="Shandy", url="https://vk.com/shandeika", icon_url="https://images-ext-1.discordapp.net/external/Nifqk3jVLvmFBCoVz1hauEOemI9X2MJPAGByFf5xpBk/%3Fsize%3D512/https/cdn.discordapp.com/avatars/335464992079872000/9c00b41b1efbc4fd02dce40ff5469bc0.png")
    embed.add_field(name="Изменения", value="1. Перед и после ника стоит 🎄\n2. Перед и после названия сервера стоит 🎄", inline=False)
    embed.add_field(name="Если вы готовы, то для начала процесса необходимо ввести", value="`.start`", inline=True)
    embed.add_field(name="Для отмены всех действий нужно ввести", value="`.reset`", inline=True)
    embed.add_field(name="ОЧЕНЬ ВАЖНО!\nРазмести роль бота выше всех!", value="Иначе он не сможет изменять ники", inline=True)
    embed.set_footer(text="Copyright © 2019–2020 Shandy developer agency All Rights Reserved. © 2020")
    await guild.owner.send(embed=embed)



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
