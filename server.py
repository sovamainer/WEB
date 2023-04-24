import discord
from discord.ext import commands
import logging
import random
from youtube_dl import YoutubeDL
import discord.ui
import asyncio
import time
from discord import app_commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

config = {
    'token': '',
    'prefix': '$',
}

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


@bot.event
async def on_ready():
    f = open('data.txt', 'r+')
    f.truncate(0)
    print(f'{bot.user.name} запустился и готов к работе!')


# ИНФОРМАЦИЯ
@bot.command()
async def userinfo(ctx, member: discord.Member):
    user = member

    embed = discord.Embed(title="Информация о пользователе", description=f"Вся информация пользователя {user}",
                          colour=user.colour)
    embed.set_thumbnail(url=user.avatar.url)
    embed.add_field(name="Имя", value=user.name, inline=True)
    embed.add_field(name="Никнейм", value=user.nick, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Статус", value=user.status, inline=True)
    embed.add_field(name="Ведущая роль", value=user.top_role.name, inline=True)
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $userinfo\n')
    f.write('-------------------------------------------\n')
    f.close()
    await ctx.send(embed=embed)


@bot.command()
async def servinfo(ctx):
    name = str(ctx.guild.name)
    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon.url)
    embed = discord.Embed(
        title=name + " Server Info",
        color=discord.Color.random()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Владелец", value=owner, inline=True)
    embed.add_field(name="ID сервера", value=id, inline=True)
    embed.add_field(name='Создан в:', value=ctx.guild.created_at.strftime('Day: %d/%m/%Y Hour: %H:%M:%S %p'),
                    inline=False)
    embed.add_field(name="Количество участников", value=memberCount, inline=True)
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $servinfo\n')
    f.write('-------------------------------------------\n')
    f.close()
    await ctx.send(embed=embed)


# ЗАДЕРЖКА_ОТПРАВКИ
@bot.command()
async def ping(ctx):
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $ping\n')
    f.write('-------------------------------------------\n')
    f.close()
    await ctx.send('Ping {0}'.format(round(bot.latency, 5)))


# ПОМОЩЬ_ПОЛЬЗОВАТЕЛЮ
@bot.command()
async def help_us(ctx):
    emb = discord.Embed(title='Навигация по командам(для остальных пользователей)', colour=discord.Colour.blue())
    emb.add_field(name='{}rand'.format(config['prefix']), value='Случайное число')
    emb.add_field(name='{}Pepe'.format(config['prefix']), value='Pepe')
    emb.add_field(name='{}CaD'.format(config['prefix']), value='Видео с животными(просто так)')
    emb.add_field(name='{}play'.format(config['prefix']), value='Включить выбранную вами песню\n'
                                                                'Следующую песню можно включить после окончания предыдущего трека и выхода бота с канала\n'
                                                                'Иначе ничего не произойдет')
    emb.add_field(name='{}stop_m'.format(config['prefix']), value='Отключить бота от звукового канала')
    emb.add_field(name='{}roll_dice (num)'.format(config['prefix']),
                  value='Бросает указанное пользователем количество кубиков')
    emb.add_field(name='{}rps (something)'.format(config['prefix']),
                  value='Игра с ботом в камень-ножницы-бумага(доступна тоько на канале rock-paper-scissors\n'
                        'После команды {}rps обязательно нужно указать один из предложенных объектов'.format(
                      config['prefix']))
    emb.add_field(name='{}avatar (user)'.format(config['prefix']), value='Выводит аваторку выбранного пользователя')
    emb.add_field(name='{}gtn (num)'.format(config['prefix']),
                  value='Игра доступна только на канале #guess-the-number\n'
                        'После команды {}rps обязательно нужно указать число'.format(config['prefix']))
    emb.add_field(name='{}ping'.format(config['prefix']), value='Вывод задержки сообщений')
    emb.add_field(name='{}servinfo'.format(config['prefix']), value='Выводит информацию о сервере')
    emb.add_field(name='{}rand_st'.format(config['prefix']), value='Случайный стикер')
    emb.add_field(name='{}userinfo'.format(config['prefix']), value='Вывод информации о пользователе')
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $help_us\n')
    f.write('-------------------------------------------\n')
    f.close()
    await ctx.send(embed=emb)


@bot.command()
@commands.has_role('Admin')
async def help_mod(ctx):
    if ctx.channel.id == 1097070214140665978:
        emb = discord.Embed(title='Навигация по командам(для модераторов канала)',
                            colour=discord.Colour.yellow())
        emb.add_field(name='{}watch_tw (url)'.format(config['prefix']),
                      value='Установка статуса: Стримит (название канала)\n'
                            'Передача трансляции')
        emb.add_field(name='{}watch_yt (url)'.format(config['prefix']),
                      value='Установка статуса: Стримит YouTube\n'
                            'Передача видеоматериала')
        emb.add_field(name='{}game (text)'.format(config['prefix']),
                      value='Установка статуса: Играет в (название игры)\n')
        emb.add_field(name='{}clear'.format(config['prefix']), value='Очистка чата')
        emb.add_field(name='{}mute (user) (reason[необязательно])'.format(config['prefix']),
                      value='Удаление возможности писать в чат')
        emb.add_field(name='{}unmute (user)'.format(config['prefix']), value='Разрешение на общение в чате')
        await ctx.send(embed=emb)
    else:
        await ctx.reply('Данная команда не работает на этом канале')
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $help_mod\n')
    f.write('-------------------------------------------\n')
    f.close()


@bot.command()
@commands.has_role('Admin')
async def help_adm(ctx):
    if ctx.channel.id == 1097070214140665978:
        emb = discord.Embed(title='Навигация по командам(только для администраторов канала)',
                            colour=discord.Colour.red())
        emb.add_field(name='{}clear'.format(config['prefix']), value='Очистка чата')
        emb.add_field(name='{}test'.format(config['prefix']), value='Просмотр ID канала')
        emb.add_field(name='{}kick (user) (reason[необязательно])'.format(config['prefix']),
                      value='Изгнать пользователя с возможным помилованием')
        emb.add_field(name='{}ban (user) (reason[необязательно])'.format(config['prefix']),
                      value='Отправить пользователя в дальнее путешествие')
        emb.add_field(name='{}unban (user)'.format(config['prefix']),
                      value='Прощение пользователя')
        emb.add_field(name='{}giverole (user) (role)'.format(config['prefix']),
                      value='Дает роль, выбранную администратором')
        emb.add_field(name='{}remrole (user) (role)'.format(config['prefix']),
                      value='Убирает роль у пользователя, выбранную администратором')
        emb.add_field(name='{}mtm'.format(config['prefix']),
                      value='Перемещает всех пользователей на определенный канал, где находится администратор')
        emb.add_field(name='{}nickname (user) (nick)'.format(config['prefix']),
                      value="Присваивание выбранному пользователю нового nickname'а")
        await ctx.send(embed=emb)
    else:
        await ctx.reply('Данная команда не работает на этом канале')
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $help_adm\n')
    f.write('-------------------------------------------\n')
    f.close()


# РАБОТА_С_ПОЛЬЗОВАТЕЛЕМ
@bot.command()
async def avatar(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar.url
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $avatar {member}\n')
    f.write('-------------------------------------------\n')
    f.close()
    await ctx.send(userAvatar)


@bot.command()
async def rand(ctx, *args):
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $rand\n')
    f.write('-------------------------------------------\n')
    f.close()
    await ctx.reply(random.randint(0, 1000000))


dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']


@bot.command()
async def roll_dice(ctx, count):
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $roll_dice {count}\n')
    f.write('-------------------------------------------\n')
    f.close()
    res = [random.choice(dashes) for _ in range(int(count))]
    await ctx.send(" ".join(res))


@bot.command()
async def Pepe(ctx):
    stick = random.choice(('<a:5376pepepoggerschains:1099581005628706836>', '<a:3716pepedrink:1099580977531068436>',
                           '<a:3330pepescam:1099580928671625296>', '<a:3254pepepoggerditto:1099580917384744980>',
                           '<a:3135pepegamble:1099580873378111529>', '<a:1649pepehappychat:1099580125600829450>',
                           '<a:1899pepepoop:1099580841581096970>', "https://i.imgur.com/Hab3RJO.jpg"))
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $Pepe\n')
    f.write('-------------------------------------------\n')
    f.close()
    await ctx.send(stick)


@bot.command()
async def help_me(ctx):
    embed = discord.Embed(title='ОБЯЗАТЕЛЬНО \nК ПРОСМОТРУ', colour=discord.Colour.blue())
    embed.add_field(name='', value='https://www.youtube.com/watch?v=XQYNUwYHV1c')
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $help_me\n')
    f.write('-------------------------------------------\n')
    f.close()
    await ctx.reply(embed=embed)


@bot.command()
async def gtn(ctx, num):
    if ctx.channel.id == 1099337790086451230:
        botChoise = random.randint(1, 50)
        if int(num) == botChoise:
            await ctx.send(f'Точное попадание!\n'
                           f'У меня было число {botChoise}\n'
                           f'У тебя было число {num}')
        elif abs(int(num) - botChoise) <= 5:
            await ctx.send(f'Было близко...\n'
                           f'У меня было число {botChoise}\n'
                           f'У тебя было число {num}')
        else:
            await ctx.send(f'Неудача. Попробуй еще раз!\n'
                           f'У меня было число {botChoise}\n'
                           f'У тебя было число {num}')
    else:
        await ctx.reply('Данная команда не работает на этом канале')
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $gtn {num}\n')
    f.write('-------------------------------------------\n')
    f.close()


# ЗАДАЧИ_МОДЕРА_АДМИНА
@bot.command()
@commands.has_role("Moderation")
async def clear(ctx, amount=100):
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $clear\n')
    f.write('-------------------------------------------\n')
    f.close()
    await ctx.channel.purge(limit=amount)


@bot.command()
@commands.has_role('Admin')
async def test(ctx):
    await ctx.send(ctx.channel.id)


# РАБОТА_С_ПОЛЬЗОВАТЕЛЕМ
@bot.command()
async def CaD(ctx):
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $CaD\n')
    f.write('-------------------------------------------\n')
    f.close()
    await ctx.send('https://i.imgur.com/FZEztL9.mp4')


@bot.command(help="Play with .rps [your choice]")
async def rps(ctx, rps):
    if ctx.channel.id == 1097079482814304386:
        rpsGame = ['камень', 'бумага', 'ножницы']
        await ctx.send(f"Камень, ножницы или бумага? Выбирайте с умом...")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame

        user_choice = rps

        comp_choice = random.choice(rpsGame)
        if user_choice == 'камень':
            if comp_choice == 'камень':
                await ctx.send(
                    f'Что ж, это было странно. Мы сыграли вничью.\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}')
            elif comp_choice == 'бумага':
                await ctx.send(
                    f'Хорошая попытка, но в тот раз я выиграл!!\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}')
            elif comp_choice == 'ножницы':
                await ctx.send(
                    f"О, ты победил меня. Этого больше не повторится!\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}")

        elif user_choice == 'бумага':
            if comp_choice == 'камень':
                await ctx.send(
                    f'Перо побеждает меч? Больше похоже на то, что бумага бьет камень!!\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}')
            elif comp_choice == 'бумага':
                await ctx.send(
                    f'О, безумие. Мы только что сравняли счет. Я объявляю матч-реванш!!\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}')
            elif comp_choice == 'ножницы':
                await ctx.send(
                    f"О, чувак, тебе действительно удалось победить меня.\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}")

        elif user_choice == 'ножницы':
            if comp_choice == 'камень':
                await ctx.send(
                    f'хаха!! Я ТОЛЬКО ЧТО РАЗДАВИЛ ТЕБЯ!! Я зажигаю!!\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}')
            elif comp_choice == 'бумага':
                await ctx.send(f'Братан. >: |\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}')
            elif comp_choice == 'ножницы':
                await ctx.send(f"Ну что ж, мы пытались.\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}")
    else:
        await ctx.reply('Данная команда не работает на этом канале')
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $rps {rps}\n')
    f.write('-------------------------------------------\n')
    f.close()


# МУЗЫКА
@bot.command()
async def play(ctx, *url):
    if ctx.channel.id == 1098948139710419066:
        if 'музыка' in str(ctx.author.voice.channel):
            vc = await ctx.message.author.voice.channel.connect()
            a = ''.join([*url])
            with YoutubeDL(YDL_OPTIONS) as ydl:
                if 'https://' in a:
                    info = ydl.extract_info(a, download=False)
                else:
                    info = ydl.extract_info(f"ytsearch:{' '.join([*url])}", download=False)['entries'][0]
            link = info['formats'][0]['url']

            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=link, **FFMPEG_OPTIONS))
            while vc.is_playing():
                await asyncio.sleep(1)
            else:
                await asyncio.sleep(5)
                while vc.is_playing():
                    break
                else:
                    await vc.disconnect()
        else:
            await ctx.reply('Данная команда не работает на этом звуковом канале')
    else:
        await ctx.reply('Данная команда не работает на этом канале')
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $play\n')
    f.write('-------------------------------------------\n')
    f.close()


@bot.command()
async def stop_m(ctx):
    if ctx.channel.id == 1098948139710419066:
        server = ctx.message.guild
        voice_channel = server.voice_client
        await voice_channel.disconnect()
    else:
        await ctx.reply('Данная команда не работает на этом канале')
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $stop_m\n')
    f.write('-------------------------------------------\n')
    f.close()


# ЗАДАЧА_МОДЕРАЦИИ
@bot.command()
@commands.has_role('Moderation')
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True,
                                          read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Замучен {member.mention}. Причина: {reason}")
    await member.send(f"Ты был замучен на сервере {guild.name}. Причина: {reason}")


@bot.command()
@commands.has_role('Moderation')
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"Размучен {member.mention}")
    await member.send(f"Ты был размучен на сервере {ctx.guild.name}")


@bot.command()
@commands.has_role('Moderation')
async def watch_tw(ctx, mes):
    if ctx.channel.id == 1085410017504677921:
        await ctx.send('Меняю активность')
        a = mes
        mes = str(mes).split('/')
        mes1 = mes[-1]
        await bot.change_presence(activity=discord.Streaming(name=mes1, url=a))
    else:
        await ctx.reply('Данная команда не работает на этом канале')


@bot.command()
@commands.has_role('Moderation')
async def watch_yt(ctx, mes):
    if ctx.channel.id == 1085410017504677921:
        await ctx.send('Меняю активность')
        await bot.change_presence(activity=discord.Streaming(name="YouTube", url=mes))
    else:
        await ctx.reply('Данная команда не работает на этом канале')


@bot.command()
@commands.has_role('Moderation')
async def game(ctx, *mes):
    if ctx.channel.id == 1085410017504677921:
        await ctx.send('Меняю активность')
        await bot.change_presence(activity=discord.Game(name=' '.join([*mes])))
    else:
        await ctx.reply('Данная команда не работает на этом канале')


# РАБОТА_АДМИНИСТРАЦИИ
@bot.command()
@commands.has_role('Admin')
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.channel.id == 1085410017504677921 or ctx.channel.id == 1099340896245403848:
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} удален с сервера')
    else:
        await ctx.reply('Данная команда не работает на этом канале')


@bot.command()
@commands.has_role('Admin')
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.channel.id == 1085410017504677921 or ctx.channel.id == 1099340896245403848:
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} отправлен в чистилище')
    else:
        await ctx.reply('Данная команда не работает на этом канале')


@bot.command()
@commands.has_role('Admin')
async def unban(ctx, *, member):
    bannedUsers = [entry.user async for entry in ctx.guild.bans()]
    name, discriminator = member.split("#")

    for bans in bannedUsers:
        user = bans

        if (user.name, user.discriminator) == (name, discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} был разбанен.")


@bot.command(pass_context=True)
@commands.has_role('Admin')
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"{ctx.author.name}, {user.name} был одарен ролью {role.name}")


@bot.command(pass_context=True)
@commands.has_role('Admin')
async def remrole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f"{ctx.author.name}, {user.name} был лишён роли {role.name}")


@bot.command()
@commands.has_role('Admin')
async def mtm(ctx):
    await ctx.send(f'Перемещаю всех на канал {ctx.author.voice.channel}')
    for channel in ctx.guild.voice_channels:
        for member in channel.members:
            if str(member)[:-5] != str(bot.user.name):
                await member.move_to(ctx.author.voice.channel)


@bot.command(pass_context=True)
@commands.has_role('Admin')
async def nickname(ctx, member: discord.Member, *args):
    await ctx.send(f'Теперь никнейм {member}:')
    embed = discord.Embed(title=f'{" ".join([*args])}', colour=discord.Colour.random())
    await ctx.send(embed=embed)
    await member.edit(nick=' '.join([*args]))


# РАБОТА_ПОЛЬЗОВАТЕЛЯМИ
@bot.command()
async def love(ctx):
    stick = random.choice(["<:5589omenheart:1099416209692311663>", "<:6537sovalovevalorant:1099416036383674530>"])
    await ctx.send(stick)


@bot.command()
async def rand_st(ctx):
    await ctx.send(
        random.choice(('<a:5376pepepoggerschains:1099581005628706836>', '<a:3716pepedrink:1099580977531068436>',
                       '<a:3330pepescam:1099580928671625296>', '<a:3254pepepoggerditto:1099580917384744980>',
                       '<a:3135pepegamble:1099580873378111529>', '<a:1649pepehappychat:1099580125600829450>',
                       '<a:1899pepepoop:1099580841581096970>', "https://i.imgur.com/Hab3RJO.jpg",
                       '<a:emoji_3:1099415573517045880>', '<a:emoji_2:1099415293580824636>',
                       '<:6537sovalovevalorant:1099416036383674530>',
                       '<:5589omenheart:1099416209692311663>',
                       '<:xarosh1:1099414882929086604>', '<:7930omenkick:1099416377053421709>',
                       '<:2615valorantfire:1099417012096225381>', '<:1715pepehelp:1099580341569720441>',
                       '<:2312_PepoTirsk:1099580852498858015>', '<:3170pepestop:1099580903384162314>',
                       '<:4482pepehi:1099580987194740797>', '<:4687pepeangrycry:1099580995910504559>',
                       '<:5432pepegambling:1099581014717771887>', '<:5457pepeiseeu:1099581024314339338>',
                       '<:5854pepefishing:1099581033885749248>')))
    f = open('data.txt', 'a+')
    f.write('-------------------------------------------\n')
    f.write(f'{time.strftime("Day: %d/%m/%Y Hour: %H:%M:%S %p")}\n')
    f.write(f'{ctx.author} ({ctx.author.top_role.name})\n')
    f.write(f'Команда: $rand_st\n')
    f.write('-------------------------------------------\n')
    f.close()


bot.run(config['token'])
