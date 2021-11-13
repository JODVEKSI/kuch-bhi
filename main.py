import asyncio
import discord
from discord import member
from discord import guild
from discord import colour
from discord import channel
from discord.abc import _Overwrites
from discord.embeds import Embed
from discord.errors import ClientException
from discord.ext import commands
import sys
import calendar
from operator import itemgetter
from platform import python_version
from discord.flags import Intents
from psutil import *
import psutil
import traceback
import os
import time
from datetime import timedelta, datetime
import data
from utils import *
import random
import datetime
from discord.utils import get
import re
import json
import intents





def get_years(timeBetween, year, reverse):
    years = 0

    while True:
        if reverse:
            year -= 1
        else:
            year += 1

        year_days = 366 if calendar.isleap(year) else 365
        year_seconds = year_days * 86400

        if timeBetween < year_seconds:
            break

        years += 1
        timeBetween -= year_seconds

    return timeBetween, years, year

def get_months(timeBetween, year, month, reverse):
    months = 0

    while True:
        month_days = calendar.monthrange(year, month)[1]
        month_seconds = month_days * 86400

        if timeBetween < month_seconds:
            break

        months += 1
        timeBetween -= month_seconds

        if reverse:
            if month > 1:
                month -= 1
            else:
                month = 12
                year -= 1
        else:
            if month < 12:
                month += 1
            else:
                month = 1
                year += 1

    return timeBetween, months

def getReadableTimeBetween(first, last, reverse=False):
    timeBetween = int(last-first)
    now = datetime.now()
    year = now.year
    month = now.month

    timeBetween, years, year = get_years(timeBetween, year, reverse)
    timeBetween, months = get_months(timeBetween, year, month, reverse)

    weeks   = int(timeBetween/604800)
    days    = int((timeBetween-(weeks*604800))/86400)
    hours   = int((timeBetween-(days*86400 + weeks*604800))/3600)
    minutes = int((timeBetween-(hours*3600 + days*86400 + weeks*604800))/60)
    seconds = int(timeBetween-(minutes*60 + hours*3600 + days*86400 + weeks*604800))
    msg = ""

    if years > 0:
        msg += "1 year, " if years == 1 else "{:,} years, ".format(years)
    if months > 0:
        msg += "1 month, " if months == 1 else "{:,} months, ".format(months)
    if weeks > 0:
        msg += "1 week, " if weeks == 1 else "{:,} weeks, ".format(weeks)
    if days > 0:
        msg += "1 day, " if days == 1 else "{:,} days, ".format(days)
    if hours > 0:
        msg += "1 hour, " if hours == 1 else "{:,} hours, ".format(hours)
    if minutes > 0:
        msg += "1 minute, " if minutes == 1 else "{:,} minutes, ".format(minutes)
    if seconds > 0:
        msg += "1 second, " if seconds == 1 else "{:,} seconds, ".format(seconds)

    if msg == "":
        return "0 seconds"
    else:
        return msg[:-2]



client = commands.Bot(command_prefix= '>')
startTime = int(time.time())

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Activity(
    type=discord.ActivityType.listening, name=f'@>'))
  print(f"[+] READY")



@client.event
async def on_guild_join(guild):
    log_channel = client.get_channel(897462153030819840)
    user = client.get_user(int(829186804824539176))
    channel = guild.text_channels[0]
    invite = await channel.create_invite(unique=True)
    embed = discord.Embed(title="Astron", color=data.color, description=f"Joined A New Server!")
    embed.add_field(name='Server Name', value=f'**{guild.name}**', inline=False)
    embed.add_field(name='Server Owner', value=f'**{guild.owner}**', inline=False)
    embed.add_field(name="Total Members", value=f"**{len(guild.members)}**", inline=False)
    embed.add_field(name="Invite Link", value=invite, inline=False)
    embed.add_field(name="Now We Are In", value=f"{len(client.guilds)} Servers")
    embed.set_thumbnail(url=guild.icon_url)
    await log_channel.send(embed=embed)
    await user.send(embed=embed)

'''@client.command(aliases=["botinfo"])
async def stats(ctx):
  total_members = [x.id for x in client.get_all_members()]
  total_channels = [x.id for x in client.get_all_channels()]
  text_channel_list = []
  for guild in client.guilds:
    for channel in guild.text_channels:
      text_channel_list.append(channel)
  voice_channel_list = []
  for guild in client.guilds:
    for channel in guild.voice_channels:
      voice_channel_list.append(channel)
  proc = Process()
  cpuThred = os.cpu_count()
  cpu_usage = psutil.cpu_percent(interval=1)
  memStats = psutil.virtual_memory()
  memPerc = memStats.percent
  memUsed = memStats.used
  memTotal = memStats.total
  memUsedGB = "{0:.1f}".format(((memUsed / 1024) / 1024) / 1024)
  memTotalGB = "{0:.1f}".format(((memTotal/1024)/1024)/1024)
  mem_total = virtual_memory().total / (1024**2)
  mem_of_total = proc.memory_percent()
  mem_usage = mem_total * (mem_of_total / 100)
  currentTime = int(time.time())
  timeString  = getReadableTimeBetween(startTime, currentTime)
  embed = discord.Embed(description=f"**[{data.name}](https://discord.gg/AEudgTx546)**", color=data.color2, inline=False)
  embed.set_author(name="Synix#0005", icon_url="https://cdn.discordapp.com/avatars/829186804824539176/effc4c276203f4ca6060631379552022.png?size=1024")
  embed.add_field(name="Cpu Stats", value=f"Usage - {cpu_usage}%\nThreads - {cpuThred}", inline=False)
  embed.add_field(name="Servers", value=f"{len(client.guilds)}", inline=False)
  embed.add_field(name="Members", value=f"{len(total_members)} Total", inline=False)
  embed.add_field(name="Channels", value=f"{len(total_channels)} Total\n{len(text_channel_list)} Text\n{len(voice_channel_list)} Voice", inline=False)
  embed.add_field(name="Memory Stats", value=f"Total Memory - {memTotalGB} GB\nPercent - {memPerc}%\nUsed - {memUsedGB} GB\nUsage - {mem_usage:,.3f} / {mem_total:,.0f} GB ({mem_of_total:.0f}%)", inline=False)
  embed.add_field(name="Ping", value=f"Websocket - {int(client.latency * 1000)}ms", inline=False)
  embed.add_field(name="Uptime", value=f"{timeString}", inline=False)
  embed.add_field(name="Developers", value=f"{data.developers}", inline=False)
  embed.add_field(name="Language", value=f"Python {python_version()}", inline=False)
  embed.set_footer(text=f"Made with discord.py {python_version()}", icon_url="https://images-ext-1.discordapp.net/external/0KeQjRAKFJfVMXhBKPc4RBRNxlQSiieQtbSxuPuyfJg/http/i.imgur.com/5BFecvA.png")
  await ctx.send(embed=embed)'''

@client.command()
async def ping(ctx):
    await ctx.send(f'Latency is {round(client.latency * 1000)} ms')

'''@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} Has Banned')'''

''' @client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
            return '''

class  DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ['s', 'm']:
            return(int(amount), unit)

            raise commands.BadArgument(message='Not a valid duration')



@client.command()
@commands.has_permissions(ban_members = True)
async def tempban(ctx, member : commands.MemberConverter, duration: DurationConverter):
    multiplier = {'s': 1, 'm': 60}
    amount, unit = duration
    await ctx.guild.ban(member)
    await ctx.send(f'{member} Has Been Banned For {amount}{unit}')
    await asyncio.sleep(amount * multiplier [unit])
    await ctx.guild.unban(member)

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : commands.MemberConverter, reason = None):
    await ctx.guild.ban(member)
    await ctx.send(f'{member} Has Been Banned')


@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : commands.MemberConverter, reason = None):
    await ctx.guild.kick(member)
    await ctx.send(f'{member} Has Been Kicked')

@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Missing Permissions")
        await ctx.message.delete()



'''@client.command()
async def gstart(ctx, t, message, *, prize):
    await ctx.message.delete()
    winerscount = int(message)

    seconds = ("s", "sec", "secs", 'second', "seconds")
    minutes = ("m", "min", "mins", "minute", "minutes")
    hours = ("h", "hour", "hours")
    days = ("d", "day", "days")
    weeks = ("w", "week", "weeks")


    try:
        temp = re.compile("([0-9]+)([a-zA-Z]+)")
        if not temp.match(t):
            return await ctx.send("You did not specify a unit of time, please try again.")
        res = temp.match(t).groups()
        time = int(res[0])
        since = res[1]

    except ValueError:
        return await ctx.send("You did not specify a unit of time, please try again.")

    if since.lower() in seconds:
        timewait = time
    elif since.lower() in minutes:
        timewait = time * 60
    elif since.lower() in hours:
        timewait = time * 3600
    elif since.lower() in days:
        timewait = time * 86400
    elif since.lower() in weeks:
        timewait = time * 604800
    else:

        return await ctx.send("You did not specify a unit of time, please try again.")

    futuredate = datetime.utcnow() + timedelta(seconds=timewait)
    embed1 = discord.Embed(color=0xFF0F00, timestamp=futuredate, description=f'**<a:gw3:885406439009562684> {prize} <a:gw3:885406439009562684>**\n\nReact with <a:gw:885406322647007283> to participate\n\n**__Giveaway Information__**\n\n<a:gw2:885406382625542186> **Winner(s): {message}\n<a:gw2:885406382625542186> Hosted by: {ctx.author.mention}\n**\n\n**__Giveaway Winners__**\n\n<a:gw2:885406382625542186> Not Decided.')

    embed1.set_footer(text=f"Giveaway Will End")
    msg = await ctx.channel.send(embed=embed1)
    await msg.add_reaction("<a:gw:885406322647007283>")
    await asyncio.sleep(timewait)
    message = await ctx.channel.fetch_message(msg.id)
    for reaction in message.reactions:
        if str(reaction.emoji) == "<a:gw:885406322647007283>":
            users = await reaction.users().flatten()
            if len(users) == 1:
                return await msg.edit(embed=discord.Embed(title="Nobody has won the giveaway."))
    try:
        winners = random.sample([user for user in users if not user.bot], k=winerscount)
    except ValueError:
        return await ctx.channel.send("not enough participants")
    winnerstosend = "\n".join([winner.mention for winner in winners])

    win = await msg.edit(embed=discord.Embed(description=f"**<a:gw3:885406439009562684> GIVEAWAY ENDED <a:gw3:885406439009562684>**\n\n\n\n**__Giveaway Winners__**\n\n**<a:gw2:885406382625542186> Giveaway Winner(s): {winnerstosend}\n<a:gw2:885406382625542186> Hosted by: {ctx.author.mention}\n<a:gw2:885406382625542186> Prize(s): {prize}\n**",
                                             color=0xFF0F00))
    mg = f"Hey {winnerstosend} <a:LcDecExclamation:882864036872593408>"
    await ctx.channel.send(mg, embed=discord.Embed(description=f"**<a:gw:885406322647007283> Congratulations {winnerstosend}, you have won [giveaway](https://discordapp.com/channels/{ctx.guild.id}/{ctx.channel.id}/{msg.id}) of {prize} <a:gw:885406322647007283>**",
                                             color=0xFF0F00))'''

@client.command()
async def addrole(ctx, role: discord.Role,  member: discord.Member):
    if ctx.author.guild_permissions.administrator:
        await member.add_roles(role)
        await ctx.send(f"Successfully Given {role.mention} To {member.mention}")
        await ctx.message.add_reaction('👍')

@client.command()
async def removerole(ctx, role : discord.Role, member : discord.Member):
    if ctx.author.guild_permissions.administrator:
        await member.remove_roles(role)
        await ctx.send(f"Successfully Removed {role.mention} From {member.mention}")
        await ctx.message.add_reaction('👍')

'''@client.event
async def on_member_join(member):
    channel = client.get_channel(897445945950752808)

    em=discord.Embed(
        title=f'Welcome',
        description=f'{member.mention} Joined {member.guild.name}',
        color=discord.Color.random(),
        timestamp=datetime.utcnow()
        ).add_field(
        name=f':hey: Rules',
        value=f'<#798887148509593600>'
        ).add_field(
        name=f':hey: Chat',
        value='<#826387689472917515>'
        ).add_field(
        name=f'Total members',
        value=f'{member.guild.member_count}'
        ).set_footer(text=f'{member.name} just joined')

    await channel.send(embed=em)'''


@client.command()
async def announce(ctx, channel: discord.TextChannel, *, msg):
   # await ctx.send('Successful.')
    await channel.send(f'{msg}')

@client.command()
@commands.has_permissions(manage_channels = True)
async def cs(ctx):
    channel = ctx.channel
    embed = discord.Embed(title=f"Stats for **{channel.name}**", discription=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}")
    embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
    embed.add_field(name="Channel Id", value=channel.id, inline=False)
    embed.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No Topic.'}", inline=False)
    embed.add_field(name="Channel Position", value=channel.position, inline=False)
    embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False)
    embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=False)
    embed.add_field(name="Channel is news?", value=channel.is_news(), inline=False)
    embed.add_field(name="Channel Creation Time", value=channel.created_at, inline=False)
    embed.add_field(name="Channel Permissions Synced", value=channel.permissions_synced, inline=False)
    embed.add_field(name="Channel Hash", value=hash(channel), inline=True)

    embed.color = 0x2F3136


    await ctx.send(embed=embed)
'''
@client.group(invoke_without_command=True)
@commands.guild_only()
@commands.has_permissions(manage_channels=True)
async def new(ctx):
    await ctx.send("Invalid sub-command passed")'''

'''

@new.command()
@commands.guild_only()
@commands.has_permissions(manage_channels=True)
async def category(ctx, role: discord.Role, *, name):
    _Overwrites = {
        ctx.guild.default_role: discord.PermissionsOverwrite(read_message=False),
        ctx.guild.me: discord.PermissionsOverwrite(read_message=True),

    }'''

@client.command()
async def dc(ctx, channel : discord.TextChannel):
    embed = discord.Embed(
        title = 'Succeess',
        description = f'Channel: {channel} Has Been Deleted',
    )
    if ctx.author.guild_permissions.manage_channels:
        await ctx.send(embed=embed)
        await channel.delete()

        Intents = discord.Intents.default()
        intents.member = True
        client = discord.client(intents=intents)



@client.command()
async def createchannel(ctx, channelName):
    guild = ctx.guild

    embed = discord.Embed(
        title = 'Success',
        description = "{} Has Been Successfully Created".format(channelName)
    )
    if ctx.author.guild_permissions.manage_channels:
        await guild.create_text_channel(name='{}'.format(channelName))
        await ctx.send(embed=embed)

@client.command()
async def poll(ctx, *, message):
    embed = discord.Embed(title = "POLL", description = f"{message}")
    msg=await ctx.channel.send(embed=embed)
    await msg.add_reaction(' 👍 ')
    await msg.add_reaction(' 👎 ')


'''@client.command()
async def uptime(ctx):
    currentTime = int(time.time())
    timeString  = getReadableTimeBetween(startTime, currentTime)
    Latest  = time.asctime(time.localtime(time.time()))
    await ctx.send(f'Uptime: {timeString}\nLatest Restart: {Latest}')'''

extensions = ['cogs.info',  'cogs.invite', 'cogs.afk', 'cogs.utils', 'cogs.Events']
if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
            print(f"LOADED: {extension}")
        except Exception as e:
            print(f"Error loading: {extension}")
            traceback.print_exc()

client.run("ODkyMDcyNjU2MDc2MTYxMDg0.YVHlZw.EHoTBvO3fJAd4qBmsNLjR0H2tKY")
