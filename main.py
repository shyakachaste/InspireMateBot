import discord
import os
import aiohttp
import json
import random
from replit import db
from keep_alive import keep_alive
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="$", intents=intents)

sad_words = [
    "sad", "depressed", "unhappy", "angry", "miserable", "depressing",
    "frustrated", "overwhelmed", "burnout", "stressed", "disheartened",
    "downhearted", "demotivated", "hopeless"
]

starter_encouragements = [
    "Cheer up! 😊", "Hang in there. 🌈", "You are a great person! 🚀",
    "Stay strong, you got this! 💪",
    "Remember, mistakes are the stepping stones to success. 🚧"
]

programming_motivation = [
    "Keep coding, you're making progress! 💻",
    "Programming is like magic, and you're the wizard! 🧙",
    "Errors are just opportunities to learn. Keep going! 🛠️",
    "The best way to learn programming is by doing. Code on! 🚀",
    "Every line of code you write is a step towards mastery. 📈",
    "Success in programming is all about persistence and problem-solving. You're on the right track! 🔍",
    "Embrace the bugs! They are the challenges that make you a better coder. 🐞",
    "You're not just writing code; you're crafting a solution to a problem. How cool is that? 😎",
    "Programming is a journey, not a destination. Enjoy the process! 🌟",
    "Your code might have errors, but your potential is limitless. Keep pushing boundaries! 🌐"
]

if "encouragements" not in db.keys():
    db["encouragements"] = starter_encouragements


async def get_quote():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://zenquotes.io/api/random") as response:
            if response.status == 200:
                json_data = await response.json()
                quote = json_data[0]['q'] + " -" + json_data[0]['a']
                return quote
            else:
                return "Could not retrieve a quote at the moment, please try again later."


def update_encouragements(encouraging_message):
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements


def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command(name='inspire')
async def inspire(ctx):
    quote = await get_quote()
    await ctx.send(quote)


@bot.command(name='new')
async def new(ctx, *, encouraging_message: str):
    update_encouragements(encouraging_message)
    await ctx.send("New encouraging message added. 🌟")


@bot.command(name='del')
async def delete(ctx, index: int):
    encouragements = db["encouragements"]
    if 0 <= index < len(encouragements):
        delete_encouragement(index)
        await ctx.send(f"Deleted message at index {index}.")
    else:
        await ctx.send("Index out of range.")


@bot.command(name='list')
async def list_encouragements(ctx):
    encouragements = db["encouragements"]
    await ctx.send('\n'.join(f'{i}: {msg}'
                             for i, msg in enumerate(encouragements)))


@bot.command(name='motivate')
async def motivate(ctx):
    await ctx.send(random.choice(programming_motivation))


@bot.command(name='commands')
async def custom_help(ctx):
    help_message = """Commands:
    $inspire - Get an inspirational quote
    $new [message] - Add a new encouraging message
    $del [index] - Delete an encouraging message at the specified index
    $list - List all encouraging messages
    $motivate - Get motivation for programming
    $commands - Display this help message"""
    await ctx.send(help_message)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(db["encouragements"]))

    await bot.process_commands(message)

    if "awesome" in msg:
        await message.add_reaction('🚀')
        await message.channel.send("You're awesome! 🎉")


keep_alive()
bot.run(os.getenv('TOKEN'))
