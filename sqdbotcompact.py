import discord
from discord.ext.commands import Bot
from discord.ext import commands
from mortar import findTarget
from search import searchLayers
import asyncio
import re

# SET CONSTS
BOT_PREFIX = ("?", "!")
TOKEN = ""

# CREATE BOT
client = Bot(command_prefix=BOT_PREFIX)

# CREATE ?search and !search
@client.command(name="search",
                description="Searches Squad layers for maps that meet certain parameters. For help with usage type: \n\n ?search help")
async def search(terms, *request):
    if request:
        output = searchLayers(terms, request, "discord")
        #print("Request: "+request)
    else:
        output = searchLayers(terms, False, "discord")
    await client.say(formatForDiscord(output))

# CREATES ?mortar and !mortar
@client.command(name="mortar")
async def mortar(mortar, target):
    await client.say(findTarget(mortar, target))
    
# Adds discord indention
def formatForDiscord(inString):
    output = inString.replace("<>","```").replace("</>","```")
    return output

# Starts the bot
client.run(TOKEN)
