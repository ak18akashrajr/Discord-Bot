import discord
import os
import requests
import json
import random
from replit import db
from alive_bot import keep_alive

client = discord.Client()

sad_words = ["sad","depressed","depressing","unhappy","bad","bad day","miserable","sogam","bad guy"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!",
  "Don't Worry",
  "Hey , Don't Worry It would be good",
  "Don't Feel Bad about that😀",
  "All is well😀",
  "You're to here do a great thing",
  "Nalladhae Nadakum😅",
  "Poda Andavanae namba pakam irukan 😅"

]




if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
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

  msg = message.content
  if message.content.startswith("Hello"):
    await message.channel.send("Hey There How's it going?")
  elif message.content.startswith("Hi"):
    await message.channel.send("Hey There How's it going?")

  if msg.startswith('Inspire me'):
    quote = get_quote()
    await message.channel.send(quote)

  if(message.content=="Thanks"):
    await message.channel.send("Hey you're my friend dude😊")

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN'))









  

 
  

  
