import discord
from discord.ext import commands
import logging
import random
import os
from youtube_dl import YoutubeDL
import discord.ui
import asyncio

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

config = {
    'token': 'token',
    'prefix': '$',
}

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


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
    emb.add_field(name='{}role_dice'.format(config['prefix']),
                  value='Бросает указанное пользователем количество кубиков')
    await ctx.send(embed=emb)


@bot.command()
@commands.has_permissions(administrator=True)
async def help_adm(ctx):
    if ctx.channel.id == 1097070214140665978:
        emb = discord.Embed(title='Навигация по командам(только для администраторов канала)',
                            colour=discord.Colour.red())
        emb.add_field(name='{}clear'.format(config['prefix']), value='Очистка чата')
        emb.add_field(name='{}test'.format(config['prefix']), value='Просмотр ID канала')
        emb.add_field(name='{}kick'.format(config['prefix']), value='Изгнать пользователя с возможным помилованием')
        emb.add_field(name='{}ban'.format(config['prefix']), value='Отправить пользователя в дальнее путешествие')
        emb.add_field(name='{}giverole'.format(config['prefix']), value='Дает роль, выбранную администратором')
        emb.add_field(name='{}remrole'.format(config['prefix']),
                      value='Убирает роль у пользователя, выбранную администратором')
        await ctx.send(embed=emb)
    else:
        await ctx.reply('Данная команда не работает на этом канале')


@bot.command()
async def rand(ctx, *args):
    await ctx.reply(random.randint(0, 1000000))


dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']


@bot.command()
async def roll_dice(ctx, count):
    res = [random.choice(dashes) for _ in range(int(count))]
    await ctx.send(" ".join(res))


@bot.command()
async def help_me(ctx):
    if ctx.channel.id == 1097070214140665978:
        embed = discord.Embed(title='ОБЯЗАТЕЛЬНО \nК ПРОСМОТРУ', colour=discord.Colour.blue())
        embed.add_field(name='', value='https://www.youtube.com/watch?v=XQYNUwYHV1c')
        await ctx.reply(embed=embed)
    else:
        await ctx.reply('Данная команда не работает на этом канале')


@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


@bot.command()
@commands.has_permissions(administrator=True)
async def test(ctx):
    await ctx.send(ctx.channel.id)


@bot.command()
async def Pepe(ctx):
    await ctx.send("https://i.imgur.com/Hab3RJO.jpg")


@bot.command()
async def CaD(ctx):
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


class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Button", style=discord.ButtonStyle.gray)
    async def gray_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=f"This is an edited button response!")


@bot.command()
async def button(ctx):
    await ctx.send("This message has buttons!", view=Buttons())


@bot.command()
async def play(ctx, url):
    if ctx.channel.id == 1098948139710419066:
        vc = await ctx.message.author.voice.channel.connect()
        print(url)
        with YoutubeDL(YDL_OPTIONS) as ydl:
            if 'https://' in url:
                info = ydl.extract_info(url, download=False)
            else:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
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
        await ctx.reply('Данная команда не работает на этом канале')


@bot.command()
async def stop_m(ctx):
    if ctx.channel.id == 1098948139710419066:
        server = ctx.message.guild
        voice_channel = server.voice_client
        await voice_channel.disconnect()
    else:
        await ctx.reply('Данная команда не работает на этом канале')


@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.channel.id == 1085410017504677921:
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} удален с сервера')
    else:
        await ctx.reply('Данная команда не работает на этом канале')


@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.channel.id == 1085410017504677921:
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} отправлен в чистилище')
    else:
        await ctx.reply('Данная команда не работает на этом канале')


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"{ctx.author.name}, {user.name} был одарен ролью {role.name}")


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def remrole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f"{ctx.author.name}, {user.name} был лишён роли {role.name}")


bot.run(config['token'])
