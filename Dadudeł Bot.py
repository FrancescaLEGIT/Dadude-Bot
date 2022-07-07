import discord
from discord.ext import commands
import random
from random import choice
from itertools import cycle
import os
import json
import random
import datetime
import requests
import aiosqlite
import asyncio
from typing import Text
from discord.ext import tasks
from discord.ext.commands import clean_content
import aiohttp
import platform
from aiohttp import ClientSession
import time
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="+",intents=intents)
bot.version = "1.0"
bot.remove_command('help')
@bot.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send(f"**Pong! {round(bot.latency * 1000)}ms**")
@bot.command(name="invite")
async def invite(ctx: commands.Context):
    await ctx.send(" **Witaj jeżeli chcesz mnie dodać na swój serwer tutaj masz link https://discord.com/api/oauth2/authorize?client_id=644193729456111636&permissions=8&scope=bot !**")
@bot.command(name="Support")
async def Support(ctx: commands.Context):
    await ctx.send(" **Jeżeli chcesz dowiedzieć się informacji dotyczących bota uzyskać pomoc czy popisać z ludzmi to masz tutaj link do serwera support https://discord.gg/8mvNYcWTDm link do serwera 2 twórcy bota https://discord.gg/XEcKWgM9eE !**")
@bot.command(aliases=['clean', 'limpar'])
async def clear(ctx, n=0):
  if n <= 0:
    await ctx.send('**Musisz podać liczbę wiadomości do usunięcia**')
  else:
    await ctx.channel.purge(limit=int(n))
    x = discord.Embed(title='Czysty system!')
    x.add_field(name='Usunięte wiadomości:', value=f'{n}')
    x.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    x.timestamp = datetime.datetime.utcnow()
    msg = await ctx.send(embed=x)

@bot.command(aliases=['Ban'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'''"{member}" **został zbanowy!** **przez** "{ctx.author}" **powód bana** "{reason}"''')   

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason==None:
      reason="**admin ma zawsze racje!**"

    await ctx.guild.kick(member)
    await ctx.reply(f'**użytkownik** {member.mention} **został kicknienty z powódu** {reason}')
@bot.command(description="Wycisza/mutuje określonego użytkownika..")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="muted", description=f"{member.mention} został wyciszony ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" zostałeś wyciszony: {guild.name} powód: {reason}")
@bot.command(description="unmutuje/odcisza określonego użytkownika. ")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f" zostałeś od mutowany: - {ctx.guild.name}")
   embed = discord.Embed(title="unmute", description=f" Odmutowanie -{member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def poll(ctx, *, content:str):
  print("Twerzenie z wyborem Tak/Nie Ankiety..")
  #create the embed file
  embed=discord.Embed(title=f"{content}", description="Zareaguj emotką ✅ oznacza Tak, ❌ Oznacza nie.",  color=0xd10a07)
  #set the author and icon
  embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url) 
  print("Embed created")
  #send the embed 
  message = await ctx.channel.send(embed=embed)
  #add the reactions
  await message.add_reaction("✅")
  await message.add_reaction("❌")

@bot.group(invoke_without_command= True)

async def pomoc(ctx):
    # insert your help command embed or message here
    embed= discord.Embed(title="Pomoc", description="Lista komend")
    embed.add_field(name="Moderacyjne", value="+pomoc moderacyjne")
    embed.add_field(name="Ważne", value="+pomoc ważne")
    embed.add_field(name="Przydatne", value="+pomoc przydatne")
    embed.add_field(name="zabawa", value="+pomoc zabawa")
    embed.add_field(name="leveling", value="+pomoc leveling")
    embed.add_field(name="svstats", value="+pomoc svstats")
    await ctx.send(embed=embed)
@pomoc.command()

async def moderacyjne(ctx):
    embed= discord.Embed(title="Moderacyjne", description="lista moderacyjnych komend")
    embed.add_field(name="Komendy", value="ban, kick, mute, clear, poll, Warn")
    await ctx.send(embed=embed)
@pomoc.command()

async def ważne(ctx):
    embed= discord.Embed(title="Ważne", description="lista ważnych komend")
    embed.add_field(name="Komendy", value="invite, Support, botinfo, yt, instagram")
    await ctx.send(embed=embed)
@pomoc.command()

async def przydatne(ctx):
    embed= discord.Embed(title="Przydatne", description="lista Przydatnch komend")
    embed.add_field(name="Komendy", value="say, ping, svinfo, losuj, usinfo, avatar, przypomnienie")
    await ctx.send(embed=embed)    
@pomoc.command()

async def zabawa(ctx):
    embed= discord.Embed(title="zabawa", description="lista For Fun komend")
    embed.add_field(name="Komendy", value="pies, rickroll, rzutmonetą, meme")
    await ctx.send(embed=embed) 
@pomoc.command()

async def leveling(ctx):
    embed= discord.Embed(title="leveling", description="lista levelingowych komend")
    embed.add_field(name="Komendy", value="NIE MA NARAZIE KOMEND")
    await ctx.send(embed=embed)    
@pomoc.command()

async def svstats(ctx):
    embed= discord.Embed(title="Svtats", description="lista svstats komend")
    embed.add_field(name="Komendy", value="statyinfo numberOfChannel, statyinfo memberCount, statyinfo name, statyinfo rolesCount")
    await ctx.send(embed=embed)    

@bot.command(name='say')
async def audit(ctx, msg=None):
    if msg is not None:
        await ctx.send(msg)
@bot.command()
async def svinfo(ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f'{guild} informacje o serwerze ', description="info o serwerze",
                          timestamp=ctx.message.created_at, color=discord.Color.red())
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="Liczba kanałów :", value=len(guild.channels))
        embed.add_field(name="Liczba ról:", value=len(guild.roles))
        embed.add_field(name="Liczba boostów:", value=guild.premium_subscription_count)
        embed.add_field(name="Liczba członków ı:", value=guild.member_count)
        embed.add_field(name="Rok Utworzenia serwera:", value=guild.created_at)
        embed.add_field(name="Właściciel serwera :", value=guild.owner)
        embed.set_footer(text=f"Komenda {ctx.author} używany przez.", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
@bot.command()
async def losuj(ctx):

    # checks the author is responding in the same channel
    # and the message is able to be converted to a positive int
    def check(msg):
        return msg.author == ctx.author and msg.content.isdigit() and \
               msg.channel == ctx.channel

    await ctx.send("**Podaj liczbe**")
    msg1 = await bot.wait_for("message", check=check)
    await ctx.send("**Wpisz drugą, większą liczbę**")
    msg2 = await bot.wait_for("message", check=check)
    x = int(msg1.content)
    y = int(msg2.content)
    if x < y:
        value = random.randint(x,y)
        await ctx.send(f"**dostałeś liczbe {value}.**")
    else: 
        await ctx.send(" :exclamation: **upewnij się, że pierwsza liczba jest mniejsza niż druga liczba** :exclamation: **.** ")
@bot.command()
async def pies(ctx):
   r = requests.get("https://dog.ceo/api/breeds/image/random")
   json_data = r.json()
   dog = json_data['message'] 
   embed=discord.Embed(color=0xff0000)
   embed.add_field(name ="1.", value="piesek", inline=False)
   embed.set_image(url=dog)
   await ctx.reply(embed=embed)
@bot.command()
async def rickroll(ctx):
    embed=discord.Embed(title="Zostałeś z rickrollowany lmao!", url="", description="**To przystojny Rick Astley **", color=0x966908)
    embed.set_image(url="https://c.tenor.com/u9XnPveDa9AAAAAM/rick-rickroll.gif")
    await ctx.reply(embed=embed)  
@bot.event
async def on_message_join(member):
    channel = client.get_channel(channel_id)
    embed=discord.Embed(title=f"Witaj na srwerze {member.name}", description=f"Dzięki za dołączenie {member.guild.name}!") 
    embed.set_thumbnail(url=member.avatar_url) 
    await channel.send(embed=embed)
@bot.command()
async def botinfo(ctx):
    """
    Przydatna komenda wyświetlające statystyki bota.
    """
    pythonVersion = platform.python_version()
    dpyVersion = discord.__version__
    serverCount = len(bot.guilds)
    memberCount = len(set(bot.get_all_members()))

    embed = discord.Embed(title=f'{bot.user.name} Statystyki', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embed.add_field(name='Wersja Bota:', value=bot.version)
    embed.add_field(name='Wersja Pythona:', value=pythonVersion)
    embed.add_field(name='Wersja Discord.py', value=dpyVersion)
    embed.add_field(name='Serwery na których jestem:', value=serverCount)
    embed.add_field(name='wszyscy użytkownicy z serweerów na kórych jestem:', value=memberCount)
    embed.add_field(name='Developerzy Bota:', value="<@573662244076912641>")

    embed.set_footer(text=f"Nazwa Bota | {bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)
@bot.command(aliases=['Warn'])
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    await ctx.send(f'''**{member}** **został ostrzeżony**  **powód ostrzeżennia** **{reason}**''')     
@bot.command()
async def statyinfo(ctx, info):
    server = ctx.guild
    if info == "memberCount":
        await ctx.send(server.member_count)
    elif info == "numberOfChannel":
        await ctx.send(len(server.voice_channels) + len(server.text_channels))
    elif info == "name":
        await ctx.send(server.name) 
    elif info == "rolesCount":
        await ctx.send(len(server.roles)-1) 
    else:
        await ctx.send("Dziwne... tego nie wiem")

messageCount = {}

@bot.event
async def on_message(ctx):
    author = str(ctx.author)
    if author in messageCount:
        messageCount[author] += 1
    else:
        messageCount[author] = 1
    
    await bot.process_commands(ctx)
 
@bot.command()
async def messages(ctx: commands.Context, *, user: discord.User=None):
    """Aby zobaczyć, ile wiadomości wysyła użytkownik"""
    user = user or ctx.author
    msg = messageCount.get(str(user))
    if msg:
        await ctx.send(f"{user} wysłał lącznie {msg} ")
    else:
        await ctx.send(f"{user} nie wysłał jeszcze żadnej wiadomości")
@bot.event
async def update_data(users, user): #
    if not user.id in users: #i called this in the member join event
      users[user.id] = {}
      users[user.id]['points'] = 0
@bot.event
async def add_points(ctx, users, user, pts): #I wrote that function at the beginning of the script
      users[user.id]['points'] += pts
@bot.command(pass_context = True)
async def give(ctx, member, amount):
      with open('users.json', 'r') as f:
        users =  json.load(f)
        await add_points(users, member, amount) 
      with open('users.json', 'w') as f:                      
        json.dump('users', 'f') 
      await ctx.send(f'given {member} {amount} programming points')
@bot.command(aliases=["usinfo"])
async def userinfo(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"Informacje o użytkowniku - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Na wniosek {ctx.author}")

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Wyświetlana nazwa:", value=member.display_name)

    embed.add_field(name="Utworzono konto:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Dołączono na serwer:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Role:", value="".join([role.mention for role in roles]))
    embed.add_field(name="Najwyższa rola:", value=member.top_role.mention)
    print(member.top_role.mention)
    await ctx.send(embed=embed)
@bot.command(name="yt")
async def yt(ctx: commands.Context):
    await ctx.send(" **Witam oto mój kanał na yt https://www.youtube.com/channel/UCYQaJd-ed_1lBqMXxjRO9TA!**")
@bot.command(name="instagram")
async def instagram(ctx:commands.Context):
    await ctx.send("**Witam oto mój instagram https://www.instagram.com/wiktoria_dobrek/ **")
@bot.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)
determine_flip = [1, 0]

@bot.command()
async def rzutmonetą(ctx):
    if random.choice(determine_flip) == 1:
        embed = discord.Embed(title="rzutmonetą | (Agumarine)", description=f"{ctx.author.mention} Rzuciłeś monetą, wypadło **orzeł**!")
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="rzutmonetą | (Agumarine)", description=f"{ctx.author.mention} Rzuciłeś monetą, wypadło **reszka**!")
        await ctx.send(embed=embed)
@bot.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed) 
@bot.command()
async def przypomnienie(ctx, time, *, task):
    def convert(time):
        pos = ['s', 'm', 'h', 'd']

        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}

        unit = time[-1]

        if unit not in pos:
            return -1
        try:
            val = int(time[:-1])
        except:
            return -2

        return val * time_dict[unit]
    converted_time = convert(time)
    if converted_time == -1:
        await ctx.send('Nie odpowiedziałeś poprawnie na godzinę')
        return
    if converted_time == -2:
        await ctx.send('Czas musi być liczbą całkowitą, a przy okazji nienawidzę matematyki')
        return

    await ctx.send(f'Ustawiłem przypomnienie dla {task}, i wybuchnie w {time}')

    await asyncio.sleep(converted_time)
    await ctx.author.send(f'Ustawiłeś przypomnienie dla {task}, OVER AND OUT! 3 ')
    await ctx.author.send(f'Ustawiłeś przypomnienie dla {task}, OVER AND OUT! 2 ')
    await ctx.author.send(f'Ustawiłeś przypomnienie dla {task}, OVER AND OUT! 1 ')
    await ctx.author.send(f'Przypomnienie dla {task} to koniec.') 
bot.run("NjQ0MTkzNzI5NDU2MTExNjM2.XcweKQ.QfOdAWa0VpSfsJKkxh6lV_SGaeo")   
