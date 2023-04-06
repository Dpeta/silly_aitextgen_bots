import os
import random
import logging

import discord
from aitextgen import aitextgen

from utility import allowedMentions, intents

logger = logging.getLogger(__name__)
rust_ai = aitextgen(
    model_folder=os.path.join("rustye2", "rustmodel"),
    tokenizer_file=os.path.join("rustye2", "rustmodel", "aitextgen.tokenizer.json"),
)
rust_quote = (
    "fiwst thing i noticed abouwt u: "
    "'now thewe's a wady who couwwd wesowve any buwtton-based dispuwtes,' i thouwght. "
)
rust_activity = discord.Game(rust_quote)
rust = discord.Client(
    intents=intents,
    activity=rust_activity,
    allowed_mentions=allowedMentions,
    member_cache_flags=discord.MemberCacheFlags.none(),
    max_messages=None,
)


@rust.event
async def on_ready():
    print(f"We have logged in as {rust.user}")


@rust.event
async def on_message(message):
    try:
        await rust_bot.message(message)
    except Exception:
        logger.exception("rust on_message exception")


class RustBot:
    def __init__(self, client):
        self.client = client

    async def message(self, message):
        if message.author == self.client.user:
            return
        elif self.client.user.mentioned_in(message) or message.content.startswith("!r"):
            await message.channel.typing()

            channel_msg_str = message.content

            channel_msg_str = channel_msg_str.replace("!r ", "")
            channel_msg_str = channel_msg_str.replace("!r", "")
            channel_msg_str = "---\n" + channel_msg_str

            print("channel_msg_str = " + channel_msg_str)
            # generated_message = channel_msg_str

            t = random.uniform(0.8, 1.0)
            temperature_increase = 1.05
            output = ""
            while not output.strip():
                print(t)
                output = rust_ai.generate_one(
                    temperature=t,
                    prompt="\n\n" + channel_msg_str,
                    repetition_penalty=1.19,
                    max_length=256,
                )
                print(output)
                temperature_increase = pow(temperature_increase, 1.1)
                t += temperature_increase * 0.1

            output = output.split("---\n")[1]
            output = output.strip()
            await message.channel.send(output, allowed_mentions=allowedMentions)


rust_bot = RustBot(rust)
