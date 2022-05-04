from copy import deepcopy
import json
import logging
import discord
from google.cloud import secretmanager

ROLE_MESSAGE_ID = 971407813580558368
EMOJI_TO_ROLE = {
    "penguincheer": 971410906909114388,
    "ravenhappy": 971377298269945886
}

POWER_USERS = ["Pronyo#1078"]

logging.basicConfig(level=logging.INFO)


# Get token with google secret manager
secret_manager = secretmanager.SecretManagerServiceClient()
token = secret_manager.access_secret_version(request={"name": "projects/4264716284/secrets/discord-token/versions/1"}).payload.data.decode("UTF-8")

intents = discord.Intents.default()
intents.members = True

discord_client = discord.Client(intents=intents)

@discord_client.event
async def on_ready():
    print("=======================================")
    print('We have logged in as {0.user}'.format(discord_client))
    print("=======================================")

'''
Add roles to users when selecting a reaction.
'''
@discord_client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    print(payload)
    if payload.message_id != ROLE_MESSAGE_ID:
        return

    guild = discord_client.get_guild(payload.guild_id)
    if guild is None:
        return

    try:
        role_id = EMOJI_TO_ROLE[payload.emoji.name]
    except KeyError:
        return

    role = guild.get_role(role_id)
    if role is None:
        return

    try:
        await payload.member.add_roles(role)
    except discord.HTTPException:
        pass

'''
Remove roles from users that deselect a reaction.
'''
@discord_client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    print(payload)
    if payload.message_id != ROLE_MESSAGE_ID:
        return
        
    guild = discord_client.get_guild(payload.guild_id)
    if guild is None:
        return

    try:
        role_id = EMOJI_TO_ROLE[payload.emoji.name]
    except KeyError:
        return

    role = guild.get_role(role_id)
    if role is None:
        return

    member = guild.get_member(payload.user_id)
    if member is None:
        return

    try:
        await member.remove_roles(role)
    except discord.HTTPException:
        pass


'''
Handle custom commands.
'''
@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    if message.content.startswith("!help"):
        await message.channel.send('Hello!')
    
    if message.content.startswith("!roleinit") and str(message.author) in POWER_USERS:
        penguin = discord.utils.get(discord_client.emojis, name="penguincheer")
        raven = discord.utils.get(discord_client.emojis, name="ravenhappy")

        embed = discord.Embed(
            title="PaperBot Role Assignment",
            description= f'\
                Assign yourself a race role so you can get notified about races in your timezone! \n \n \
                {penguin} for Racer (US)\n \
                {raven} for Racer (EU)', 
            color=discord.Colour.from_rgb(223, 178, 255)
        )
 
        messageEmbed = await message.channel.send(embed=embed)
        await messageEmbed.add_reaction(penguin)
        await messageEmbed.add_reaction(raven)

discord_client.run(token)
