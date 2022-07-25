from sre_constants import SUCCESS
from discord import AllowedMentions
import nextcord
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext import commands
from nextcord import Intents
import os
import time
import calendar
import datetime
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
nextcord.http._modify_api_version(9)
bot = commands.Bot(command_prefix=["<@999760430052417638> ", "a.", "A."], case_insensitive=True,intents=intents)
dankMoon = 710573788856582225

class verifyButtons(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value=None
    
    @nextcord.ui.button(label="Verify!",style=nextcord.ButtonStyle.green,emoji="✅")
    async def verify(self, button:nextcord.ui.button,interaction:nextcord.Interaction):
        guild = bot.get_guild(710573788856582225)
        verified = guild.get_role(741336292612243603)
        if verified in interaction.user.roles:
            await interaction.response.send_message(ephemeral=True,content="You are already verified...")
        else:
            await interaction.user.add_roles(verified)
            await interaction.response.send_message(ephemeral=True,content="You have been verfied!")
            general = bot.get_channel(710573789309698060)
            mentions = nextcord.AllowedMentions(everyone=False,users=True,roles=False)
            await general.send(f"Everyone welcome {interaction.user.mention} to the server!\nIf you are looking for a heist, it will probably be in <#711435197807067156> :slight_smile:",allowed_mentions=mentions,delete_after=120)
        self.value = True

@bot.event # This event prints in the console when the bot has logged in
async def on_ready():
    print(f'We have logged in as {bot.user}')
    channel = await bot.fetch_channel(996446872451432498)
    startupEmbed = nextcord.Embed(title="The bot has started!", description="Hi **Stones**! The bot has now started. Feel free to use `a.help` to see what I can do!",color=nextcord.Color.magenta())
    startupEmbed.set_thumbnail("https://cdn.discordapp.com/attachments/996446872451432498/999801982770491522/dank_moon.png")
    await channel.send(embed=startupEmbed)
    verificationChannel = bot.get_channel(741336727188144148)
    embed = nextcord.Embed(title="Verification",description="Click the button below to get verified!",color=nextcord.Color.green())
    await verificationChannel.purge(limit=5,check=lambda m:m.author==bot.user)
    view = verifyButtons()
    await verificationChannel.send(embed=embed,view=view)
    await view.wait()

@commands.has_role(805719483930771477)
@bot.command()
async def verification(ctx):
    embed = nextcord.Embed(title="Verification",description="Click the button below to get verified!",color=nextcord.Color.green())
    await ctx.channel.purge(limit=1)
    view = verifyButtons()
    await ctx.send(embed=embed,view=view)
    await view.wait()

@bot.slash_command(name="avatar",description="View a user's avatar",guild_ids=[dankMoon])
async def avatar(interaction:Interaction,user:nextcord.User=None):
    if user == None:
        user = interaction.user
    embed = nextcord.Embed(title=f"Avatar of {user}", color=nextcord.Color.magenta())
    if user.avatar != None:
        embed.set_image(url=str(user.avatar))
    else:
        embed.set_image(url=user.default_avatar)
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name="ping",description="🏓 Shows the bot's latency",guild_ids=[dankMoon])
async def ping(interaction:Interaction):
    embed = nextcord.Embed(title="Pong! 🏓",description=f"{round(bot.latency * 1000, 1)}ms",color=nextcord.Color.magenta())
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_member_join(member):
    embed = nextcord.Embed(title=f"Welcome to Dank Moon, {member}!",description=f"To get started in the server, read the rules in <#710840207808659517> and verify in <#741336727188144148>",color=nextcord.Color.magenta())
    embed.add_field(name="Once you have verified...",value="+ Get pings and other roles from <#711952053433401375>!\n+ Select your colour role in <#710847274988732507>!\n+ Chat with us in <#710573789309698060>!\n+ Our heists take place in <#711435197807067156>!\n+ See what we are giving away in <#711435312332537889> and <#809422611452919818>!")
    embed.set_footer(text="If you are here for a heist, don't freeload! We ban freeloaders :P")
    embed.set_thumbnail("https://cdn.discordapp.com/attachments/996446872451432498/999801982770491522/dank_moon.png")
    await member.send(embed=embed)
    rulesChan = bot.get_channel(710840207808659517)
    await rulesChan.send(f"{member.mention}",delete_after=1)

@bot.slash_command(name="userinfo",description="View cool information about a Discord user",guild_ids=[dankMoon])
async def userinfo(interaction:Interaction,user:nextcord.User=None):
    if user == None:
        user = interaction.user
    embed = nextcord.Embed(color=nextcord.Color.magenta(),title=user.display_name)
    if user.avatar != None:
        embed.set_author(name=f"{user}",icon_url=str(user.avatar.url))
    else:
        embed.set_author(name=f"{user}",icon_url=str(user.default_avatar.url))
    embed.set_thumbnail(str(user.display_avatar.url))
    if user.banner != None:
        embed.set_image(str(user.banner.url))
    embed.set_footer(text=f"ID: {user.id}")
    embed.add_field(name="Account Created",value=f"{user.created_at.year}-{user.created_at.month}-{user.created_at.day} at {user.created_at.hour}:{user.created_at.minute}:{user.created_at.second} {user.created_at.tzinfo}")
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name="whois",description="View cool information about another member of the server",guild_ids=[dankMoon])
async def whois(interaction:Interaction,member:nextcord.Member=None):
    if member == None:
        member = interaction.user
    embed = nextcord.Embed(color=member.top_role.color,title=member.display_name)
    if member.avatar != None:
        embed.set_author(name=member,icon_url=member.avatar.url)
    else:
        embed.set_author(name=member,icon_url=member.default_avatar.url)
    embed.set_thumbnail(member.display_avatar.url)
    if member.banner != None:
        embed.set_image(member.banner.url)
    embed.set_footer(text=f"ID: {member.id}")
    embed.add_field(name="Account Created",value=f"{member.created_at.year}-{member.created_at.month}-{member.created_at.day} at {member.created_at.hour}:{member.created_at.minute}:{member.created_at.second} {member.created_at.tzinfo}\n<t:{calendar.timegm([member.created_at.year,member.created_at.month,member.created_at.day,member.created_at.hour,member.created_at.minute,member.created_at.second])}:R>")
    embed.add_field(name="Joined Server",value=f"{member.joined_at.year}-{member.joined_at.month}-{member.joined_at.day} at {member.joined_at.hour}:{member.joined_at.minute}:{member.joined_at.second} {member.joined_at.tzinfo}\n<t:{calendar.timegm([member.joined_at.year,member.joined_at.month,member.joined_at.day,member.joined_at.hour,member.joined_at.minute,member.joined_at.second])}:R>")
    embed.add_field(name="Is a bot?",value=str(member.bot))
    if len(member.roles) <= 40:
        embed.add_field(name="Roles",value=f"{str(len(member.roles))}: {str(member.roles)}",inline=False)
    else:
        embed.add_field(name="Roles",value=f"{str(len(member.roles))}: (Too many to list)",inline=False)
    embed.add_field(name="User permissions",value=str(member.guild_permissions),inline=True)
    await interaction.response.send_message(embed=embed)


bot.run("OTk5NzYwNDMwMDUyNDE3NjM4.GOfJE9.SzY__65AkGeN6rWRaTp4egYhl3gdWN6pm5my1g")