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

programming_tips = [
    "Read the documentation, it's your best friend! 📚",
    "Write code every day, even if it's just a little. ✏️",
    "Don't be afraid to ask for help. The community is here for you! 👥",
    "Practice by working on real projects. 🛠️",
    "Learn to debug. It's a valuable skill! 🔍",
    "Keep your code clean and well-commented. 🧹",
    "Version control is important. Learn Git. 🗂️",
    "Break problems into smaller, manageable tasks. 🧩",
    "Keep learning new languages and frameworks. 🌐",
    "Stay updated with the latest trends in technology. 📈"
]

if "encouragements" not in db.keys():
    db["encouragements"] = starter_encouragements


async def get_quote():
    async with aiohttp.ClientSession() as session:
        sources = [
            "https://zenquotes.io/api/random", "https://api.quotable.io/random"
        ]
        source = random.choice(sources)
        try:
            async with session.get(source) as response:
                if response.status == 200:
                    json_data = await response.json()
                    if "zenquotes" in source:
                        quote = json_data[0]['q'] + " -" + json_data[0]['a']
                    else:
                        quote = json_data['content'] + " -" + json_data[
                            'author']
                    return quote
                else:
                    print(f"Error fetching quote: {response.status}")
                    return "Could not retrieve a quote at the moment, please try again later."
        except Exception as e:
            print(f"Exception in get_quote: {e}")
            return "Could not retrieve a quote due to an error."


async def get_joke():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                    "https://official-joke-api.appspot.com/random_joke"
            ) as response:
                if response.status == 200:
                    json_data = await response.json()
                    joke = json_data['setup'] + " ... " + json_data['punchline']
                    return joke
                else:
                    print(f"Error fetching joke: {response.status}")
                    return "Could not retrieve a joke at the moment, please try again later."
        except Exception as e:
            print(f"Exception in get_joke: {e}")
            return "Could not retrieve a joke due to an error."


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
    try:
        quote = await get_quote()
        await ctx.send(quote)
    except Exception as e:
        print(f"Exception in inspire command: {e}")
        await ctx.send("Could not send the quote due to an error.")


@bot.command(name='joke')
async def joke(ctx):
    try:
        joke = await get_joke()
        await ctx.send(joke)
    except Exception as e:
        print(f"Exception in joke command: {e}")
        await ctx.send("Could not send the joke due to an error.")


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


@bot.command(name='tip')
async def tip(ctx):
    await ctx.send(random.choice(programming_tips))


@bot.command(name='commands')
async def custom_help(ctx):
    help_message = """Commands:
    $inspire - Get an inspirational quote
    $joke - Get a random joke
    $new [message] - Add a new encouraging message
    $del [index] - Delete an encouraging message at the specified index
    $list - List all encouraging messages
    $motivate - Get motivation for programming
    $tip - Get a random programming tip
    $commands - Display this help message"""
    await ctx.send(help_message)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()
    responded = False

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(db["encouragements"]))
        responded = True

    if "awesome" in msg:
        await message.add_reaction('🚀')
        await message.channel.send("You're awesome! 🎉")
        responded = True

    if not responded:
        await bot.process_commands(message)


keep_alive()
bot.run(os.getenv('TOKEN'))
