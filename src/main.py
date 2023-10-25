import time

from discord.ext import commands
import discord
import random

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
    intents=intents  # Set up basic permissions
)

bot.author_id = 278864711305658368  # Change to your discord id


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


@bot.command("ping")
async def pong(ctx):
    await ctx.send('pong')


@bot.command("name")
async def name(ctx):
    await ctx.send(ctx.author.name)


@bot.command("d6")
async def d6(ctx):
    await ctx.send(random.randint(1, 6))


@bot.command("admin")
async def admin(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Admin")
    if not role:
        role = await ctx.guild.create_role(name="Admin", permissions=discord.Permissions(8))
    await member.add_roles(role)
    await ctx.send(f"{member.mention} is now an Admin")


@bot.command("ban")
async def ban(ctx, target, reason=""):
    member = discord.utils.get(ctx.guild.members, name=target)
    if not member:
        await ctx.send(f"Member {target} not found")
        return
    if member == ctx.author:
        await ctx.send("You can't ban yourself")
        return
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("You don't have the permission to ban members")
        return
    if reason == "":
        reasons = ["I dont like u", "ICEs are not tolerated here", "You can come back if you offer me a "
                                                                   "beer", "Get out of my swamp"]
        reason = random.choice(reasons)
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned for {reason}")


FLOOD_MAP = {}
MAX_FLOOD = {5, 1}


@bot.command("flood")
async def flood(ctx, x=5, y=1):
    global FLOOD_MAP, MAX_FLOOD
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("You don't have the permission to ban members")
        return
    if FLOOD_MAP:
        await ctx.send('You can spam boys')
        FLOOD_MAP = {}
    else:
        await ctx.send('Attention, représailles si un malandrin flood le serveur')
        MAX_FLOOD = {x, y}
        FLOOD_MAP[ctx.author.name]: [time.time()]
        print('FLOOD_MAP', FLOOD_MAP)


@bot.event
async def on_message(message):
    # global FLOOD_MAP
    # print('FLOOD_MAP', FLOOD_MAP)
    # if FLOOD_MAP:
    #     print('FLOOD_MAP', FLOOD_MAP)
    #     if message.author.id in FLOOD_MAP:
    #         userId = FLOOD_MAP[message.author.id]
    #         print('userId', userId)
    #         print(FLOOD_MAP[0][message.author.id])
    #         if len(FLOOD_MAP[0][message.author.id]) >= MAX_FLOOD[0]:
    #             if FLOOD_MAP[0][message.author.id][-1] - FLOOD_MAP[0][message.author.id][0] <= MAX_FLOOD[1] * 60:
    #                 await message.channel.send(f"Be calm {message.author.mention}, or you'll get the spanky spanky")
    #         FLOOD_MAP[0][message.author.id].append(time.time())
    #     else:
    #         FLOOD_MAP[str(ctx.author.name)]: [time.time()]

    if message.content == "Salut tout le monde":
        await message.channel.send("Salut tout seul")
        await message.channel.send(message.author.mention)

    await bot.process_commands(message)


@bot.command("xkcd")
async def xkcd(ctx):
    await ctx.send("https://xkcd.com/" + str(random.randint(1, 2000)))


@bot.command("poll")
async def poll(ctx, question=""):
    if question == "":
        await ctx.send("Please enter a question")
        return
    await ctx.send("@here " + question)
    message = await ctx.send(question)
    await message.add_reaction('👍')
    await message.add_reaction('👎')


token = "MTE2Njc4NTgwNTUzNzI1NTUwNQ.GEAONS.vQBdSZ8mZP_eJjdmdCttExfHM0screIHx0WgvQ"
bot.run(token)  # Starts the bot
