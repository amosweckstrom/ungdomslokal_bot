import discord
from discord.ext import commands
from discord.utils import get
from discord import Permissions, Forbidden
from dotenv import load_dotenv
import os

load_dotenv(override=True)

print("Role ID:", os.getenv("UNGDOM_ROLE_ID"))
print("Admin ID:", os.getenv("LEDARE_ROLE_ID"))
print("Guild ID:", os.getenv("GUILD_ID"))
print("Token:", os.getenv("TOKEN"))

# Set IDs and token
role_id = int(os.getenv("UNGDOM_ROLE_ID"))
admin_id = int(os.getenv("LEDARE_ROLE_ID"))
guild_id = int(os.getenv("GUILD_ID"))
token = os.getenv("TOKEN")




# Configure intents
intents = discord.Intents.default()
intents.auto_moderation = True
intents.message_content = True

# Configure permissions
permissions_on = Permissions()
permissions_off = Permissions()

permissions_on.update(
    view_channel=True,send_messages=True, change_nickname=True, send_messages_in_threads=True,
    embed_links=True, attach_files=True, add_reactions=True, use_external_emoji=True,
    use_application_commands=True, connect=True, speak=True, stream=True,
    use_embedded_activities=True, use_voice_activation=True, request_to_speak=True, read_message_history=True
)

permissions_off.update(
    read_message_history=True,send_messages=False, change_nickname=False, send_messages_in_threads=False,
    embed_links=False, attach_files=False, add_reactions=False, use_external_emoji=False,
    use_application_commands=False, connect=False, speak=False, stream=False,
    use_embedded_activities=False, use_voice_activation=False, request_to_speak=False, view_channel=True
)

# Initialize client
client = discord.Client(intents=intents)

# Client events
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    try:
        guild = await client.fetch_guild(guild_id)
    except Forbidden:
        print("I do not have access to that guild or it doesn't exist.")

    youth_role = get(guild.roles, id=role_id)
    admin_role = get(guild.roles, id=admin_id)

    if message.content.startswith("!stäng") and admin_role in message.author.roles:
        await youth_role.edit(permissions=permissions_off)
        await message.channel.send("We are now closed!")
        print("closed")
    elif message.content.startswith("!öppna") and admin_role in message.author.roles:
        await youth_role.edit(permissions=permissions_on)
        await message.channel.send("We are now open!")
        print("open")

# Run the client
client.run(token)