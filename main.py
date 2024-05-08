import discord
from botkey import *  
from discord.ext import commands
from colorama import Back, Fore, Style
import time 
import platform
import random
import yt_dlp as youtube_dl
import asyncio 


client = commands.Bot(command_prefix = "/", intents=discord.Intents.all())
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '10.0.0.145'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume = 0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
    
    @classmethod
    async def from_url(cld, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

'''
Getting everything ready 
'''
@client.event
async def on_ready():
    prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
    print(prfx + " Logged in as " + Fore.YELLOW + client.user.name)
    print(prfx + " Bot ID " + Fore.YELLOW + str(client.user.id))
    print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
    print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
    cmds_synced = await client.tree.sync()
    print(prfx + " Slash CMDs synced " + Fore.YELLOW + str(len(cmds_synced)) + " Commands")

@client.tree.command(name="hello", description= "Says hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(content="Hello!", ephemeral=True)

@client.tree.command(name="join", description = "joins current user's voice channel")
async def join(interaction: discord.Interaction):
    channel = interaction.user.voice.channel
    await channel.connect()
    if(client.voice_clients != []):
        await interaction.response.send_message(content="Joined " + str(interaction.user.voice.channel))
    else:
        await interaction.response.send_message(content="Failed to join VC", ephemeral=True)

    #await interaction.response.send_message(content = "joined " + str(interaction.user.voice.channel), ephemeral=True)

@client.tree.command(name="play", description= "Enter a valid YouTube video link to play audio")
async def play(interaction: discord.Interaction,  url: str):
    server = interaction.guild
    channel = interaction.user.voice.channel
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_connected():
        pass
    else:
        await channel.connect()
    try :
        voice_client = interaction.guild.voice_client
        await interaction.response.send_message(content="Starting")
        async with interaction.channel.typing():
            filename = await YTDLSource.from_url(url, loop=client.loop)
            voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await interaction.edit_original_response(content='Now playing: {}'.format(filename))
    except:
        await interaction.followup.send(content='Could not play audio')

@client.tree.command(name='stop', description='Stop playing current audio')
async def stop(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    
    if voice_client.is_playing():
        await interaction.response.send_message(content="Stopping audio")
        await voice_client.stop()
        
    else:
        await interaction.response.send_message(content='The bot is not playing audio at the moment')

@client.tree.command(name='pause', description="Pause the current song")
async def pause(interaction: discord.Interaction):
    voice_client = interaction.guide.voice_client

    if voice_client.is_playing():
        await interaction.response.send_message(content="Pausing current song")
        await voice_client.pause()
    else:
        await interaction.response.send_message(content="There is nothing currently playing")

@client.tree.command(name='resume', description="Resumes playback of current song")
async def resume(interaction: discord.Interaction):
    voice_client = interaction.guide.voice_client

    if voice_client.is_paused():
        await interaction.response.send_message(content="Resuming playback")
        await voice_client.resume()
    else:
        await interaction.response.send_message(content="The bot was not playing anything before this or is not paused. Use /play <url> to play something")

'''
@client.tree.command(name='stop', description='Stops playing the current song')
async def stop(interaction: discord.Interaction):
    voice_client = interaction.guide.voice_client

    if voice_client.is_playing():
        await interaction.resopnse.send_message(content="Stopping playback")
        await voice_client.stop()
    else:
        await interaction.response.send_message("The bot is not currently playing anything. Use /play <url> to play something")
''' 
@client.event
async def on_message_delete(message):
    await message.channel.send(message.author.mention + " Deleting messages?")
    #embed = discord.Embed()
    #embed.set_image(url='https://tenor.com/view/dies-from-cringe-meme-cringe-imagine-gif-23477312')
    await message.channel.send('https://tenor.com/view/dies-from-cringe-meme-cringe-imagine-gif-23477312')


@client.command()
async def shutdown(ctx):
    await ctx.send("Cya losers")
    voice = ctx.voice_client
    await voice.disconnect()
    await client.close()

@client.command()
async def d6(ctx):
    num = random.randint(1,6)
    await ctx.send("You a rolled a " + str(num))




client.run(BOTTOKEN)


