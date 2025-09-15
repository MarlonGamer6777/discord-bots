import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

BOTNAME = "Youtube Tutorial"
os.system(f'title Not ready - Bot: {BOTNAME}')

mod_role = "Mod"
gamer_role = "Gamer"
noob_role = "Noob"
can_remove_noob_role_role = "Rem_Noob"

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='\\', intents=intents)

@bot.event
async def on_ready():
    os.system(f'title Ready! - Bot: {bot.user.name}')
    print(f"Bot is ready! Bot: {bot.user.name}")

@bot.event
async def on_member_join(member):
    print(f"{member.name} ist dem Server beigetreten!")
    await member.send(f"Willkommen auf dem Server {member.name}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # if "\\" in message.content:
    #     print(f"{message.author.name} hat {message.content} verwendet!")
    
    if "shit" in message.content.lower():
        print(f"[Filter] Nachricht von {message.author}:\n{message.content}")
        await message.delete()
        await message.channel.send(f"[Filter] {message.author.mention} hat ein böses Wort benutzt!\nBitte verwende dieses Wort nicht!")
    else:
        print(f"[{message.author}] {message.content}")
    
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hallo {ctx.author.mention}")

@bot.command()
async def be_gamer(ctx):
    if ctx.author.name == "Nanocheck":
        role = discord.utils.get(ctx.guild.roles, name=noob_role)
        if role:
            await ctx.author.add_roles(role)
            await ctx.send(f"{ctx.author.mention} wird nie ein Gamer sein... Er ist nämlich ein Noob!")
            print(f"[Rollen] {ctx.author.name} ist jetzt {role}!")
            return
        else:
            await ctx.send("xRolle existiert nicht!")
            return
    role = discord.utils.get(ctx.guild.roles, name=gamer_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} ist jetzt ein Gamer!")
        print(f"[Rollen] {ctx.author.name} ist jetzt {role}!")
    else:
        await ctx.send("Rolle existiert nicht!")

# @bot.command()
# async def assign(ctx):
#     role = discord.utils.get(ctx.guild.roles, name=secret_role)
#     if role:
#         await ctx.author.add_roles(role)
#         await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
#     else:
#         await ctx.send("Role doesn't exist")

@bot.command()
async def dont_be_gamer(ctx):
    if ctx.author.name == "Nanocheck":
        ctx.send(f"{ctx.author.mention} wid für immer ein Noob bleiben!")
        print(f"[Rollen] {ctx.author.name} hat versucht die Noob-Rolle zu entfernen!")
        return
    role = discord.utils.get(ctx.guild.roles, name=gamer_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} ist jetzt kein Gamer mehr!")
        print(f"[Rollen] {ctx.author.name} ist jetzt kein {role} mehr!")
    else:
        await ctx.send("Rolle existiert nicht!")

@bot.command()
@commands.has_role(can_remove_noob_role_role)
async def remove_noob(ctx):
    await ctx.author.remove_roles(noob_role)
    await ctx.send(f"{ctx.author.mention} ist jetzt kein Noob mehr! (Warte... das muss ein Fehler sein...)")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"{ctx.author.mention} - Du hast gesagt, dass ich\n{msg}\nsagen soll.")

@bot.command()
async def reply(ctx):
    await ctx.reply(f"{ctx.author.mention} - Antwort auf deine Nachricht") #\nNachricht:\n{ctx.content}")

@bot.command()
@commands.has_role(mod_role)
async def poll(ctx, *, question):
    if not question.endswit("?"):
        question = f"{question}?"
    embed = discord.Embed(title="Umfrage:", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(gamer_role)
async def gamer_secret(ctx):
    await ctx.send(f"Hey {ctx.author.mention}! Willkommen zum Gamer-Club!")

@gamer_secret.error
async def gamer_secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"Hey {ctx.author.mention}! Du musst Gamer sein!")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)