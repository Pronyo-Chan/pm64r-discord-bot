import discord
import logging
from google.cloud import secretmanager

logging.basicConfig(level=logging.INFO)

# Import the Secret Manager client library.
client = secretmanager.SecretManagerServiceClient()
token = client.access_secret_version(request={"name": "projects/4264716284/secrets/discord-token/versions/1"}).payload.data.decode("UTF-8")

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(token)