import discord
import os
import aiohttp
import random
from replit import db
from keep_alive import keep_alive
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="$", intents=intents)

sad_words = [
    "sad", "depressed", "unhappy", "angry", "miserable", "depressing",
    "frustrated", "overwhelmed", "burnout", "stressed", "disheartened",
    "downhearted", "demotivated", "hopeless"
]

starter_encouragements = [
    "Cheer up! 😊", "Hang in there. 🌈", "You are a great person! 🚀",
    "Stay strong, you got this! 💪", "Remember, mistakes are the stepping stones to success. 🚧"
]

if "encouragements" not in db.keys():
    db["encouragements"] = starter_encouragements

# Add this list for fortune messages
fortunes = [
    "You will have a great day today! 🌞",
    "Something exciting is coming your way! 🎉",
    "Believe in yourself and all that you are. ✨",
    "Good things take time, be patient. ⏳",
    "You will meet someone special soon. 💖",
    "Your hard work will soon pay off. 💪",
    "Unexpected good news is on its way. 📬",
    "A new opportunity will present itself to you. 🌟",
    "You are on the right path; keep going! 🚀",
    "Today is a perfect day to start something new. 🌱"
]

# Fetch a quote from an API
async def get_quote():
    async with aiohttp.ClientSession() as session:
        sources = ["https://zenquotes.io/api/random", "https://api.quotable.io/random"]
        source = random.choice(sources)
        try:
            async with session.get(source) as response:
                if response.status == 200:
                    json_data = await response.json()
                    if "zenquotes" in source:
                        quote = json_data[0]['q'] + " -" + json_data[0]['a']
                    else:
                        quote = json_data['content'] + " -" + json_data['author']
                    return quote
                else:
                    return "I couldn't fetch a quote at the moment. Try again later!"
        except:
            return "Oops! Something went wrong while fetching the quote."

# Fetch a random joke from an API
async def get_joke():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("https://official-joke-api.appspot.com/random_joke") as response:
                if response.status == 200:
                    json_data = await response.json()
                    joke = json_data['setup'] + " ... " + json_data['punchline']
                    return joke
                else:
                    return "I couldn't fetch a joke at the moment. Try again later!"
        except:
            return "Oops! Something went wrong while fetching the joke."

# Add new encouragement messages to the database
def update_encouragements(encouraging_message):
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements

# Delete an encouragement message from the database
def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="Chatting with friends!"))

@bot.command(name='inspire')
async def inspire(ctx):
    quote = await get_quote()
    await ctx.send(quote)

@bot.command(name='joke')
async def joke(ctx):
    joke = await get_joke()
    await ctx.send(joke)

@bot.command(name='new')
async def new(ctx, *, encouraging_message: str):
    update_encouragements(encouraging_message)
    await ctx.send("I've added your encouraging message! 🌟")

@bot.command(name='del')
async def delete(ctx, index: int):
    encouragements = db["encouragements"]
    if 0 <= index < len(encouragements):
        delete_encouragement(index)
        await ctx.send(f"I've deleted the message at index {index}.")
    else:
        await ctx.send("That index is out of range!")

@bot.command(name='list')
async def list_encouragements(ctx):
    encouragements = db["encouragements"]
    await ctx.send('\n'.join(f'{i}: {msg}' for i, msg in enumerate(encouragements)))

@bot.command(name='motivate')
async def motivate(ctx):
    programming_motivation = [
        "Keep coding, you're making progress! 💻",
        "Programming is like magic, and you're the wizard! 🧙",
        "Errors are just opportunities to learn. Keep going! 🛠️",
        "The best way to learn programming is by doing. Code on! 🚀",
        "Every line of code you write is a step towards mastery. 📈"
    ]
    await ctx.send(random.choice(programming_motivation))

@bot.command(name='tip')
async def tip(ctx):
    programming_tips = [
        "Read the documentation, it's your best friend! 📚",
        "Write code every day, even if it's just a little. ✏️",
        "Don't be afraid to ask for help. The community is here for you! 👥",
        "Practice by working on real projects. 🛠️",
        "Learn to debug. It's a valuable skill! 🔍"
    ]
    await ctx.send(random.choice(programming_tips))

@bot.command(name='fortune')
async def fortune(ctx):
    await ctx.send(random.choice(fortunes))

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
    $fortune - Get a random fortune cookie message
    $commands - Display this help message"""
    await ctx.send(help_message)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(db["encouragements"]))

    if "awesome" in msg:
        await message.add_reaction('🚀')
        await message.channel.send("You're awesome! 🎉")

    await bot.process_commands(message)

keep_alive()
bot.run(os.getenv('TOKEN'))
