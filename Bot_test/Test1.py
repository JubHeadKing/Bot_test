import nextcord
from nextcord.ext import commands
from nextcord.shard  import EventItem
from config import TOKEN, CLIENT_ID, CLIENT_SECRET
import wavelinkcord as wavelink

TESTING_GUILD_ID = 1111104597625421854  # Replace with your guild ID

intents = nextcord.Intents.all()
client = nextcord.Client()
bot = commands.Bot(command_prefix=".", intents=intents)

#Events
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    bot.loop.create_task(on_node())

async def on_node():

    node: wavelink.Node = wavelink.Node(uri='lavalinkinc.ml', password='incognito')
    await wavelink.NodePool.connect(client=bot, nodes=[node])
    wavelink.Player.autoplat = True

@bot.slash_command(guild_ids=[TESTING_GUILD_ID])
async def play(interaction : nextcord.Interaction, search : str):

    query = await wavelink.YouTubeTrack.search(search, return_first=True)
    destination = interaction.user.voice.channel

    if not interaction.guild.voice_client:

        vc: wavelink.Player = await destination.connect(cls=wavelink.Player)
    else:

        vc: wavelink.Player = interaction.guild.voice_client
    
    if vc.queue.is_empty and not vc.is_playing():

        await vc.play(query)
        await interaction.response.send_message(f"Ahora esta reproduciendo {vc.current.tittle}")
    
    else:
        await vc.queue.put_wait(query)
        await interaction.response.send_message(f"La cancion ha sido anadida a la lista.")

@bot.slash_command(guild_ids=[TESTING_GUILD_ID])
async def skip(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client
    await vc.stop()
    await interaction.response.send_menssage(f"Skippear xd")

@bot.slash_command(guild_ids=[TESTING_GUILD_ID])
async def pause(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client

    if vc.is_playing():

        await vc.pause()
        await interaction.response.send_message(f"Ha sido Pausado")
    else:
        await interaction.response.send_message(f"Esta Pausado")

@bot.slash_command(guild_ids=[TESTING_GUILD_ID])
async def resume(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client

    if vc.is_playing():

        await interaction.response.send_message(f"LEDS GO")
    else:
        await interaction.response.send_message(f"Reproduciendo")
        await vc.resume()

@bot.slash_command(guild_ids=[TESTING_GUILD_ID])
async def disconnect(interaction : nextcord.Interaction):
     
    vc: wavelink.Player = interaction.guild.voice_client
    await vc.disconnect()
    await interaction.response.send_message(f"Bye Bye")

@bot.slash_command(guild_ids=[TESTING_GUILD_ID])
async def queue(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client

    if not vc.queue.is_emty:

        song_counter = 0
        songs = []
        queue = vc.queue.copy()
        embed = nextcord.Embed(title="Queue")

        for song in queue:
            song_counter +=1
            song.append(song)
            embed.add_field(name-f"[{song_counter}] Duration {song.duration}", value=f"{song.title}", inline=False)

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("La lista esta vacia")
#commands
@bot.slash_command(guild_ids=[TESTING_GUILD_ID])
async def ping(interaction : nextcord.Interaction):
    latency = bot.latency * 1000  # Convertir a milisegundos
    await interaction.response.send_message(f"Pong! Latency: {latency:.2f}ms")

bot.run(TOKEN)