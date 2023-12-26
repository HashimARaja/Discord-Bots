import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


URL = 'https://official-joke-api.appspot.com/random_joke'


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = "**" + json_data[0]['q'] + "** \n- *" + json_data[0]['a'] + "*"
  return (quote)


def check_valid_status_code(request):
  if request.status_code == 200:
    return request.json()

  return False


def get_joke():
  request = requests.get(URL)
  data = check_valid_status_code(request)

  return data


def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]


def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if message.content.startswith('!hello'):
    await message.channel.send('Hello there')

  if message.content.startswith('!inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  Joke_words = ['!Joke', '!joke', '!JOKE', '!jok']
  if any(word in msg for word in Joke_words):
    joke = get_joke()

    if joke == False:
      await message.channel.send("I have ran out of jokes unfortunately...")
    else:
      await message.channel.send('**' + joke['setup'] + '!**\n' +
                                 joke['punchline'])

  if has_profanity(message.content):
    await message.channel.send("Don't use that word!")
    await message.delete()





def has_profanity(msg: str):
  api_url = 'https://api.api-ninjas.com/v1/profanityfilter?text={}'.format(msg)
  response = requests.get(api_url, headers={'X-Api-Key': 'USE YOUR API KEY HERE'})
  return response.status_code == requests.codes.ok
    
keep_alive()
client.run(os.getenv('TOKEN'))
