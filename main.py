import discord
from discord.ext import commands
import logging
import random
import os
import youtube_dl
import discord.ui

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


@bot.command()
async def rand(ctx, *args):
    await ctx.reply(random.randint(0, 1000000))


@bot.command()
async def help_me(ctx):
    if ctx.channel.id == 1097070214140665978:
        embed = discord.Embed(title='ОБЯЗАТЕЛЬНО \n К ПРОСМОТРУ', colour=discord.Colour.blue())
        embed.add_field(name='', value='https://www.youtube.com/watch?v=XQYNUwYHV1c')
        await ctx.reply(embed=embed)
    else:
        await ctx.reply('Данная команда не работает на этом канале')


@bot.command()
async def test(ctx):
    await ctx.send(ctx.channel.id)


@bot.command()
async def Pepe(ctx):
    await ctx.send("https://i.imgur.com/Hab3RJO.jpg")


@bot.command()
async def cats_and_dogs(ctx):
    await ctx.send('https://i.imgur.com/FZEztL9.mp4')


@bot.command(help="Play with .rps [your choice]")
async def rps(ctx):
    if ctx.channel.id == 1097079482814304386:
        rpsGame = ['rock', 'paper', 'scissors']
        await ctx.send(f"Rock, paper, or scissors? Choose wisely...")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame

        user_choice = await bot.wait_for('message', check=check)
        print(user_choice)

        comp_choice = random.choice(rpsGame)
        if user_choice == 'rock':
            if comp_choice == 'rock':
                await ctx.send(f'Well, that was weird. We tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'paper':
                await ctx.send(f'Nice try, but I won that time!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'scissors':
                await ctx.send(
                    f"Aw, you beat me. It won't happen again!\nYour choice: {user_choice}\nMy choice: {comp_choice}")

        elif user_choice == 'paper':
            if comp_choice == 'rock':
                await ctx.send(
                    f'The pen beats the sword? More like the paper beats the rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'paper':
                await ctx.send(
                    f'Oh, wacky. We just tied. I call a rematch!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'scissors':
                await ctx.send(
                    f"Aw man, you actually managed to beat me.\nYour choice: {user_choice}\nMy choice: {comp_choice}")

        elif user_choice == 'scissors':
            if comp_choice == 'rock':
                await ctx.send(
                    f'HAHA!! I JUST CRUSHED YOU!! I rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'paper':
                await ctx.send(f'Bruh. >: |\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'scissors':
                await ctx.send(f"Oh well, we tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}")
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


# @bot.command()
# async def play(ctx, url: str):
#    song_there = os.path.isfile("song.mp3")
#    try:
#        if song_there:
#            os.remove("song.mp3")
#    except PermissionError:
#        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
#        return
#
#    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
#    await voiceChannel.connect()
#    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#
#    ydl_opts = {
#        'format': 'bestaudio/best',
#        'postprocessors': [{
#            'key': 'FFmpegExtractAudio',
#            'preferredcodec': 'mp3',
#            'preferredquality': '192',
#        }],
#    }
#    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#        ydl.download([url])
#    for file in os.listdir("./"):
#        if file.endswith(".mp3"):
#            os.rename(file, "song.mp3")
#    voice.play(discord.FFmpegPCMAudio("song.mp3"))
#
#
# @bot.command()
# async def leave(ctx):
#    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#    if voice.is_connected():
#        await voice.disconnect()
#    else:
#        await ctx.send("The bot is not connected to a voice channel.")
#
#
# @bot.command()
# async def pause(ctx):
#    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#    if voice.is_playing():
#        voice.pause()
#    else:
#        await ctx.send("Currently no audio is playing.")
#
#
# @bot.command()
# async def resume(ctx):
#    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#    if voice.is_paused():
#        voice.resume()
#    else:
#        await ctx.send("The audio is not paused.")
#
#
# @bot.command()
# async def stop(ctx):
#    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#    voice.stop()
#

bot.run(config['token'])
