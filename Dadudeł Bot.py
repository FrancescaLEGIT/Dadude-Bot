import discord
from discord.ext import commands
from discord.ext import commands, tasks
import asyncio
from itertools import cycle
import os
import json
import random
import datetime
import requests
bot = commands.Bot(command_prefix="+")
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
    x.add_field(name='Musunięte wiadomości:', value=f'{n}')
    x.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    x.timestamp = datetime.datetime.utcnow()
    msg = await ctx.send(embed=x)

@bot.command(aliases=['Ban'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'''"{member}" **został zbanowy** "{ctx.author}" **powód bana** "{reason}"''')   

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
    embed.add_field(name="Przydatnre", value="+pomoc przydatne")
    embed.add_field(name="zabawa", value="+pomoc zabawa")
    embed.add_field(name="leveling", value="+pomoc leveling")
    await ctx.send(embed=embed)
@pomoc.command()

async def moderacyjne(ctx):
    embed= discord.Embed(title="Moderacyjne", description="lista moderacyjnych komend")
    embed.add_field(name="Komendy", value="ban, kick, mute, clear, poll")
    await ctx.send(embed=embed)
@pomoc.command()

async def ważne(ctx):
    embed= discord.Embed(title="Ważne", description="lista ważnych komend")
    embed.add_field(name="Komendy", value="invite, Support")
    await ctx.send(embed=embed)
@pomoc.command()

async def przydatne(ctx):
    embed= discord.Embed(title="Przydatne", description="lista Przydatnch komend")
    embed.add_field(name="Komendy", value="say, ping, svinfo, losuj")
    await ctx.send(embed=embed)    
@pomoc.command()

async def zabawa(ctx):
    embed= discord.Embed(title="zabawa", description="lista For Fun komend")
    embed.add_field(name="Komendy", value="pies, rickroll")
    await ctx.send(embed=embed) 
@pomoc.command()

async def leveling(ctx):
    embed= discord.Embed(title="leveling", description="lista levelingowych komend")
    embed.add_field(name="Komendy", value="rank")
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

with open("users.json", "ab+") as ab:
    ab.close()
    f = open('users.json','r+')
    f.readline()
    if os.stat("users.json").st_size == 0:
      f.write("{}")
      f.close()
    else:
      pass
 
with open('users.json', 'r') as f:
  users = json.load(f)
@bot.event    
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)
        await add_experience(users, message.author)
        await level_up(users, message.author, message)
        with open('users.json', 'w') as f:
            json.dump(users, f)
            await bot.process_commands(message)
 
async def add_experience(users, user):
  if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 0
  users[f'{user.id}']['experience'] += 6
  print(f"{users[f'{user.id}']['level']}")
 
async def level_up(users, user, message):
  experience = users[f'{user.id}']["experience"]
  lvl_start = users[f'{user.id}']["level"]
  lvl_end = int(experience ** (1 / 4))
  if lvl_start < lvl_end:
    await message.channel.send(f':tada: {user.mention} zdobyłeś poziom {lvl_end}. Gratulacje :tada:')
    users[f'{user.id}']["level"] = lvl_end
 
@bot.command()
async def rank(ctx, member: discord.Member = None):
  if member == None:
    userlvl = users[f'{ctx.author.id}']['level']
    await ctx.send(f'{ctx.author.mention} Masz poziom{userlvl}!')
  else:
    userlvl2 = users[f'{member.id}']['level']
    await ctx.send(f'{member.mention} Ma poziom {userlvl2}!')
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
bot.run("NjQ0MTkzNzI5NDU2MTExNjM2.XcweKQ.kISHDRlVlHF6NmogjNirVw77oNw")
