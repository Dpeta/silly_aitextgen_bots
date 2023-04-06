import discord


async def is_valid(output):
    """Returns True if valid and False if invalid"""
    if not output.strip():
        return False
    return True


allowedMentions = discord.AllowedMentions(
    everyone=False, users=True, roles=False, replied_user=True
)
intents = discord.Intents.none()
intents.message_content = True
intents.guild_messages = True
intents.guilds = True
intents.dm_messages = True
