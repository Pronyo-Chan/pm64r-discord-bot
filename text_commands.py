import discord
from constants import *


async def init_role_message(message, discord_client):
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

async def help_command(message):
    return await message.channel.send((
        f"To obtain racer roles and get race notifications, please react to my message in the <#{ROLE_ASSIGNMENT_CHANNEL_ID}> channel.\n"
        "I can reply to text commands starting with '!'. For a complete list of available text commands, please send **!commands**\n"
        f"For general info, <#{FAQ_CHANNEL_ID}> and <#{RESOURCES_CHANNEL_ID}> are a great place to start."
    ))

async def logic_command(message):
    return await message.channel.send((
        "Please visit the **Useful Tips** page at <https://pm64randomizer.com/tips> to view details about the randomizer's logic and other useful tips."
    ))

async def settings_command(message):
    return await message.channel.send((
        "Please visit the **Setting Details** page at <https://pm64randomizer.com/settings> to view details about the randomizer's different settings."
    ))

async def rom_command(message):
    return await message.channel.send((
        "I know very little as I don't leave the manor much... But I've heard legends mention a Paper Mario US rom in the z64 format that is perfectly compatible with the randomizer.\n"
        "Sadly, I'm afraid you're gonna have to find it on your own."
    ))

async def get_commands(message):
    return await message.channel.send((
        "The following text commands can be used to obtain information:\n\n"
        "**!help** for help about Paper Bot or the randomizer in general.\n"
        "**!logic** for details about the randomizer's logic\n"
        "**!settings** for details about the randomizer's settings\n"
        "**!rom** for info about the rom required to play the Paper Mario 64 Randomizer"
    ))