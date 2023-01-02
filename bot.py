import asyncio
import configparser
import math
from typing import Dict

import discord
from discord.ext import commands, tasks

config = configparser.ConfigParser()
config.read("config.ini", encoding='utf-8')

intents = discord.Intents.none()
intents.members = True


class WorkerData:
    def __init__(self, message_id: int, channel_id: int, percent: int):
        self.message_id = message_id
        self.channel_id = channel_id
        self.percent = percent


workers: Dict[int, WorkerData] = dict()


@tasks.loop(seconds=30)
async def update_message():
    for guild_id, worker_data in workers.items():
        guild = bot.get_guild(guild_id)
        message = await guild.get_channel(worker_data.channel_id).fetch_message(worker_data.message_id)
        embed = message.embeds[0]
        if worker_data.percent >= 100:
            embed.fields[0].value = "Закончено!"
            workers.pop(guild_id)
        else:
            embed.fields[0].value = f"{progress(worker_data.percent)} {worker_data.percent}%"
        await message.edit(embed=embed)


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        self.tree.add_command(ny)
        update_message.start()
        await self.tree.sync()


bot = MyBot(command_prefix=config['Config']['prefix'], help_command=None, intents=intents)


@discord.app_commands.guild_only()
class NewYork(discord.app_commands.Group):
    def __init__(self):
        super().__init__(name='ny', description='Новогодние команды',
                         default_permissions=discord.Permissions(permissions=8))


ny = NewYork()


def progress(percentage, width=20):
    done = math.floor(width * (percentage / 100))
    return ('█' * done) + ('░' * (width - done))


@bot.event
async def on_ready():
    print(f'Bot: {bot.user}')
    await bot.change_presence(activity=discord.Game(name=config['Config']['activity']))


@ny.command(
    name='start',
    description='Запускает процесс установки 🎄 в ники',
)
async def start(interaction: discord.Interaction):
    # Проверка на наличие сервера в исполняемых
    if interaction.guild.id in workers:
        return await interaction.response.send_message('Процесс уже запущен', ephemeral=True)
    # Формирование сообщения о запуске
    embed = discord.Embed(title='Новогоднее наступление! 🎉', description='Начинаем установку 🎄 в ники')
    embed.add_field(name='Прогресс', value=f"{progress(0)} 0%", inline=False)
    # Отправка сообщения
    message = await interaction.channel.send(embed=embed)
    # Добавление сервера в исполняемые
    workers[interaction.guild.id] = WorkerData(message.id, message.channel.id, 0)
    # Запуск процесса
    members = interaction.guild.members
    edited_members = 0
    error_members = list()
    for member in members:
        nickname = member.display_name
        if '🎄' in nickname:
            nickname = nickname.replace('🎄', '')
        if len(f'🎄 {member.display_name} 🎄') > 32:
            nickname = f"🎄 {nickname[:28]} 🎄"
        try:
            await member.edit(nick=nickname)
        except discord.Forbidden:
            print(f'Forbidden: {member.display_name}')
            error_members.append(member)
        except discord.RateLimited as rl:
            print(f'Rate Limit: {rl.retry_after} for user {member.display_name}')
            await asyncio.sleep(rl.retry_after)
            await member.edit(nick=nickname)
        edited_members += 1
        percent = int((edited_members / len(members)) * 100)
        workers[interaction.guild.id].percent = percent


@ny.command(
    name='stop',
    description='Запускает процесс удаления 🎄 из ников',
)
async def start(interaction: discord.Interaction):
    return await interaction.response.send_message('Команда выполнена', ephemeral=True)


#     if ctx.author.has_permission(Permissions.ADMINISTRATOR) is False:
#         return await ctx.send(embeds=Embed('❌ У вас нет доступа!', 'Эта команда доступна только администраторам'),
#                               ephemeral=True)
#     embed = Embed(title='✅ Запущено!', description=f'Прогресс: {progress(0)} **0%**')
#     embed.set_footer(
#         text='После завершения процесса будет прикреплен файл с пользователями, которым не удалось поменять ник')
#     message = await ctx.send(embeds=embed)
#     count = 0
#     members = list()
#     for member in ctx.guild.members:
#         count += 1
#         nick = member.display_name.replace('🎄', '')
#         nick = '🎄 ' + nick + ' 🎄'
#         if len(nick) > 30:
#             nick = '🎄 Happy New Year! 🎄'
#         try:
#             await member.edit_nickname(nick)
#         except dis_snek.errors.Forbidden:
#             members.append(member.user)
#         await asyncio.sleep(1)
#         if count % 10 == 0:
#             embed.description = f'Прогресс: {progress(int((count / ctx.guild.member_count) * 100))} **{int((count / ctx.guild.member_count) * 100)}%**'
#             await message.edit(embeds=embed)
#     embed.description = f'Прогресс: {progress(100)} **100%**'
#     file = open('members.txt', 'x+')
#     file.write('\n'.join([str(user) for user in members]))
#     file.close()
#     await message.edit(embeds=embed, file='members.txt')
#     if os.path.isfile('members.txt'):
#         os.remove('members.txt')
#     try:
#         await ctx.guild.edit(name='🎄 '+ctx.guild.name+' 🎄')
#     except:
#         pass
#
#
# @slash_command(
#     name='ny',
#     description='New year',
#     sub_cmd_name='reset',
#     sub_cmd_description='Убирает 🎄 из ников'
# )
# async def reset(ctx: InteractionContext):
#     if ctx.author.has_permission(Permissions.ADMINISTRATOR) is False:
#         return await ctx.send(embeds=Embed('❌ У вас нет доступа!', 'Эта команда доступна только администраторам'),
#                               ephemeral=True)
#     embed = Embed(title='✅ Запущено!', description=f'Прогресс: {progress(0)} **0%**')
#     embed.set_footer(
#         text='После завершения процесса будет прикреплен файл с пользователями, которым не удалось поменять ник')
#     message = await ctx.send(embeds=embed)
#     count = 0
#     members = list()
#     for member in ctx.guild.members:
#         if '🎄' not in member.display_name:
#             continue
#         count += 1
#         nick = member.display_name.replace('🎄', '')
#         try:
#             await member.edit_nickname(nick)
#         except dis_snek.errors.Forbidden:
#             members.append(member.user)
#         await asyncio.sleep(1)
#         if count % 10 == 0:
#             embed.description = f'Прогресс: {progress(int((count / ctx.guild.member_count) * 100))} **{int((count / ctx.guild.member_count) * 100)}%**'
#             await message.edit(embeds=embed)
#     embed.description = f'Прогресс: {progress(100)} **100%**'
#     file = open('members.txt', 'x+', encoding='utf-8')
#     file.write('\n'.join([str(user) for user in members]))
#     file.close()
#     await message.edit(embeds=embed, file='members.txt')
#     if os.path.isfile('members.txt'):
#         os.remove('members.txt')
#     if '🎄' in ctx.guild.name:
#         try:
#             await ctx.guild.edit(name=ctx.guild.name.replace('🎄', ''))
#         except:
#             pass


bot.run(config['Config']['token'])
