import os
import logging
import random

import discord
from aitextgen import aitextgen

from utility import is_valid, allowedMentions, intents

logger = logging.getLogger(__name__)
jasprose_ai = aitextgen(
    model_folder=os.path.join("jasprosePro", "model3"),
    tokenizer_file=os.path.join("jasprosePro", "model3", "aitextgen.tokenizer.json"),
)
jasprose_activity = discord.Activity(
    name="!j", details="!j", type=discord.ActivityType.playing
)
jasprose = discord.Client(
    intents=intents,
    activity=jasprose_activity,
    allowed_mentions=allowedMentions,
    member_cache_flags=discord.MemberCacheFlags.none(),
    max_messages=None,
)


@jasprose.event
async def on_ready():
    try:
        print("We have logged in as {0.user}".format(jasprose))
        bots = jasprose.get_channel(761301247885443105)
        file = discord.File("jasprosePro/jp_online.png", filename="jp_online.png")
        await bots.send(file=file)
    except Exception:
        logger.exception("jasprose on_ready exception")


@jasprose.event
async def on_message(message):
    try:
        await jasprose_bot.message(message)
    except Exception:
        logger.exception("jasprose on_message exception")


class JasproseBot:
    def __init__(self, client):
        self.temp = random.uniform(0.8, 1.0)
        self.client = client

    async def message(self, message):
        if message.author == self.client.user:
            return

        elif message.content.startswith("!randomness "):
            try:
                self.temp = float(message.content.strip("!randomness "))
                await message.channel.send(
                    "temp=%s" % self.temp, allowed_mentions=allowedMentions
                )
            except Exception as e:
                self.temp = random.uniform(0.8, 1.0)
                await message.channel.send(str(e), allowed_mentions=allowedMentions)

        elif self.client.user.mentioned_in(message) or message.content.startswith("!j"):
            await message.channel.typing()

            channel_msg_str = message.content

            channel_msg_str = channel_msg_str.replace("!j ", "")
            channel_msg_str = channel_msg_str.replace("!j", "")
            # channel_msg_str = channel_msg_str.replace('<@!897421712604405761>', '')

            print("channel_msg_str = " + channel_msg_str)
            # generated_message = channel_msg_str

            t = self.temp
            temperature_increase = 1.05
            output = ""
            while not await is_valid(output):
                print(t)
                output = jasprose_ai.generate_one(
                    temperature=t,
                    prompt=channel_msg_str,
                    repetition_penalty=1.19,
                    max_length=128,
                )
                print(output)
                temperature_increase = pow(temperature_increase, 1.1)
                t += temperature_increase * 0.1

            output = output.replace("martin", "marty")
            output = output.replace("Martin", "Marty")
            await message.channel.send(output, allowed_mentions=allowedMentions)


jasprose_bot = JasproseBot(jasprose)
