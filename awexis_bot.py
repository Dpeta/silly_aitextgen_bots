import os
import logging
import random

import discord
from aitextgen import aitextgen

from utility import allowedMentions, intents

logger = logging.getLogger(__name__)
awexis_ai = aitextgen(model_folder=os.path.join("weedwexis", "model"),
               tokenizer_file=os.path.join("weedwexis",
                                           "model",
                                           "aitextgen.tokenizer.json"))
awexis = discord.Client(intents=intents,
                        allowed_mentions=allowedMentions,
                        member_cache_flags=discord.MemberCacheFlags.none(),
                        max_messages=None)
@awexis.event
async def on_ready():
    print(f"We have logged in as {awexis.user}")

@awexis.event
async def on_message(message):
    try:
        await awexis_bot.message(message)
    except Exception:
        logger.exception("awexis on_message exception")
        
class AwexisBot:
    def __init__(self, client):
        self.client = client

    async def message(self, message):
        if message.author == self.client.user:
            return
        
        elif self.client.user.mentioned_in(message) or message.content.startswith('!wexis'):
            await message.channel.typing()

            channel_msg_str = message.content
            
            channel_msg_str = channel_msg_str.replace('!wexis ', '')
            channel_msg_str = channel_msg_str.replace('!wexis', '')
            #channel_msg_str = channel_msg_str.replace('<@!897421712604405761>', '')
            
            print("channel_msg_str = " + channel_msg_str)
            # generated_message = channel_msg_str

            temperature = random.uniform(0.8, 1.0)# 0.1,1
            temperature_increase = 1.05
            output = ''
            while not output.strip():
                print(temperature)
                output = awexis_ai.generate_one(temperature=temperature,
                                         prompt=channel_msg_str,
                                         repetition_penalty=1.19,
                                         max_length=128)
                print(output)
                temperature_increase = pow(temperature_increase,1.1)
                temperature += temperature_increase * 0.1


            output = output.strip(channel_msg_str)
            #output = output.split('\n')[0]
            print('b wingus')
            await message.channel.send(output,
                                       allowed_mentions=allowedMentions)
            
awexis_bot = AwexisBot(awexis)
