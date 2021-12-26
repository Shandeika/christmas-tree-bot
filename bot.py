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


@slash_command(
    name='ny',
    description='New year',
    sub_cmd_name='start',
    sub_cmd_description='Запускает процесс установки 🎄 в ники'
)
async def start(ctx: InteractionContext):
    if ctx.author.has_permission(Permissions.ADMINISTRATOR) is False:
        return await ctx.send(embeds=Embed('❌ У вас нет доступа!', 'Эта команда доступна только администраторам'),
                              ephemeral=True)
    embed = Embed(title='✅ Запущено!', description=f'Прогресс: {progress(0)} **0%**')
    embed.set_footer(
        text='После завершения процесса будет прикреплен файл с пользователями, которым не удалось поменять ник')
    message = await ctx.send(embeds=embed)
    count = 0
    members = list()
    for member in ctx.guild.members:
        count += 1
        nick = member.display_name.replace('🎄', '')
        nick = '🎄 ' + nick + ' 🎄'
        if len(nick) > 30:
            nick = '🎄 Happy New Year! 🎄'
        try:
            await member.edit_nickname(nick)
        except dis_snek.errors.Forbidden:
            members.append(member.user)
        await asyncio.sleep(1)
        if count % 10 == 0:
            embed.description = f'Прогресс: {progress(int((count / ctx.guild.member_count) * 100))} **{int((count / ctx.guild.member_count) * 100)}%**'
            await message.edit(embeds=embed)
    embed.description = f'Прогресс: {progress(100)} **100%**'
    file = open('members.txt', 'x+')
    file.write('\n'.join([str(user) for user in members]))
    file.close()
    await message.edit(embeds=embed, file='members.txt')
    if os.path.isfile('members.txt'):
        os.remove('members.txt')
    try:
        await ctx.guild.edit(name='🎄 '+ctx.guild.name+' 🎄')
    except:
        pass


@slash_command(
    name='ny',
    description='New year',
    sub_cmd_name='reset',
    sub_cmd_description='Убирает 🎄 из ников'
)
async def reset(ctx: InteractionContext):
    if ctx.author.has_permission(Permissions.ADMINISTRATOR) is False:
        return await ctx.send(embeds=Embed('❌ У вас нет доступа!', 'Эта команда доступна только администраторам'),
                              ephemeral=True)
    embed = Embed(title='✅ Запущено!', description=f'Прогресс: {progress(0)} **0%**')
    embed.set_footer(
        text='После завершения процесса будет прикреплен файл с пользователями, которым не удалось поменять ник')
    message = await ctx.send(embeds=embed)
    count = 0
    members = list()
    for member in ctx.guild.members:
        if '🎄' not in member.display_name:
            continue
        count += 1
        nick = member.display_name.replace('🎄', '')
        try:
            await member.edit_nickname(nick)
        except dis_snek.errors.Forbidden:
            members.append(member.user)
        await asyncio.sleep(1)
        if count % 10 == 0:
            embed.description = f'Прогресс: {progress(int((count / ctx.guild.member_count) * 100))} **{int((count / ctx.guild.member_count) * 100)}%**'
            await message.edit(embeds=embed)
    embed.description = f'Прогресс: {progress(100)} **100%**'
    file = open('members.txt', 'x+', encoding='utf-8')
    file.write('\n'.join([str(user) for user in members]))
    file.close()
    await message.edit(embeds=embed, file='members.txt')
    if os.path.isfile('members.txt'):
        os.remove('members.txt')
    if '🎄' in ctx.guild.name:
        try:
            await ctx.guild.edit(name=ctx.guild.name.replace('🎄', ''))
        except:
            pass


bot.start(config['Config']['token'])
