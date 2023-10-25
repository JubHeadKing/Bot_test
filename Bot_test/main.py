import nextcord
from nextcord.ext import commands
from config import TOKEN, CLIENT_ID, CLIENT_SECRET
import os
import wavelink
from wavelink.ext import spotify
import asyncio
import datetime


GUILD_ID = 1111104597625421854  # guild ID of your server

intents = nextcord.Intents.all()
client = nextcord.Client()
bot = commands.Bot(command_prefix="-", intents=intents)

#Events
@bot.event
async def on_ready() -> None:
    print(f'We have logged in as {bot.user}')
    bot.loop.create_task(setup_hook())

async def setup_hook() -> None:
        # Wavelink 2.0 has made connecting Nodes easier... Simply create each Node
        # and pass it to NodePool.connect with the client/bot.
        # Fill your Spotify API details and pass it to connect.
        sc = spotify.SpotifyClient(
            client_id='CLIENT_ID',
            client_secret='CLIENT_SECRET'
        )
        node: wavelink.Node = wavelink.Node(uri='ash.lavalink.alexanderof.xyz:2333', password='lavalink')
        await wavelink.NodePool.connect(client=bot, nodes=[node], spotify=sc)

@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.YouTubeTrack, reason):
    ctx = player.ctx
    vc: player = ctx.voice_client

    if vc.loop:
        return await vc.play(track)
    
    if vc.queue.is_empty:
        return await vc.disconnecte()
    
    next_song = vc.queue.get()
    await vc.play(next_song)
    await ctx.send(f"Now Playing: {next_song.title}")
#commands

@bot.command()
async def play(ctx: commands.Context, *, search: wavelink.YouTubeTrack):
    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Join a voice channel first lol")
    else:
        vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty and not vc.is_playing():
        await vc.play(search)
        await ctx.send(f'Playing `{search.title}`')
    else:
        await vc.queue.put_wait(search)
        await ctx.send(f'Added `{search.title}` to the queue...')
    vc.ctx = ctx
    setattr(vc, "loop", False)

bot.run(TOKEN)