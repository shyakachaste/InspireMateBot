import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

intents = discord.Intents.default()

client = discord.Client(intents=intents)

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


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote


def update_encouragements(encouraging_message):
  encouragements = db["encouragements"]
  encouragements.append(encouraging_message)
  db["encouragements"] = encouragements


def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content.lower()

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added. 🌟")

  if msg.startswith("$del"):
    encouragements = db["encouragements"]
    index = int(msg.split("$del", 1)[1])
    delete_encouragement(index)
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$motivate"):
    await message.channel.send(random.choice(programming_motivation))

  if msg.startswith("$help"):
    help_message = """Commands:
        $inspire - Get an inspirational quote
        $new [message] - Add a new encouraging message
        $del [index] - Delete an encouraging message at the specified index
        $list - List all encouraging messages
        $motivate - Get motivation for programming
        $help - Display this help message"""
    await message.channel.send(help_message)

  if "awesome" in msg:
    await message.add_reaction('🚀')
    await message.channel.send("You're awesome! 🎉")


keep_alive()
client.run(os.getenv('TOKEN'))
