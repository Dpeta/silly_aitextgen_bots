import os
import random
import logging

import discord
from aitextgen import aitextgen

from utility import allowedMentions, intents

logger = logging.getLogger(__name__)
harry_ai = aitextgen(model_folder=os.path.join("harrier2"),
                    tokenizer_file=os.path.join("harrier2",
                                                "aitextgen.tokenizer.json"))
harry = discord.Client(intents=intents,
                      allowed_mentions=allowedMentions,
                      member_cache_flags=discord.MemberCacheFlags.none(),
                      max_messages=None)

@harry.event
async def on_ready():
    print(f"We have logged in as {harry.user}")

@harry.event
async def on_message(message):
    try:
        await harry_bot.message(message)
    except Exception:
        logger.exception("harry on_message exception")

class HarryBot:
    def __init__(self, client):
        self.client = client

    async def message(self, message):
        if message.author == self.client.user:
            return
        elif self.client.user.mentioned_in(message) or message.content.startswith('!h'):
            await message.channel.typing()

            channel_msg_str = message.content.replace('!h ', '').replace('!h', '') + '.\n'
            print("channel_msg_str:\n" + channel_msg_str)

            temperature = random.uniform(0.2, 0.4)# 0.1,1
            temperature_increase = 1.05
            output = ''

            while not output.strip():
                output = harry_ai.generate_one(temperature=temperature,
                                         prompt=channel_msg_str,
                                         repetition_penalty=1.19,
                                         max_length=128/2)
                print(f"temperature: {temperature}")
                print(f"output: {output}")
                temperature_increase = pow(temperature_increase,1.1)
                temperature += temperature_increase * 0.1

            output = output.strip(channel_msg_str)
            try:
                splitter = output.split("\n")
                output = '\n'.join(splitter[:-1])
            except IndexError:
                output = splitter[0]
            await message.channel.send(output,
                                       allowed_mentions=allowedMentions)
harry_bot = HarryBot(harry)
