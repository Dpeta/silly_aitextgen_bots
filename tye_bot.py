import os

# import time
# import sys
# import subprocess
import logging
import random

import discord
from aitextgen import aitextgen

from utility import allowedMentions, intents

logger = logging.getLogger(__name__)
tye_ai = aitextgen(
    model_folder=os.path.join("tylerjack", "model"),
    tokenizer_file=os.path.join("tylerjack", "model", "aitextgen.tokenizer.json"),
)
tye = discord.Client(
    intents=intents,
    allowed_mentions=allowedMentions,
    member_cache_flags=discord.MemberCacheFlags.none(),
    max_messages=None,
)


@tye.event
async def on_ready():
    print(f"We have logged in as {tye.user}")


@tye.event
async def on_message(message):
    try:
        await tye_bot.message(message)
    except Exception:
        logger.exception("tye on_message exception")


class TyeBot:
    def __init__(self, client):
        self.client = client

    async def message(self, message):
        if message.author == self.client.user:
            return
        """
        if message.content.startswith('!ferrari'):
            await message.channel.typing()
            with open('ferrari.webm', 'rb') as src:
                read = src.read()
            length = len(read)
            output = bytearray()
            evil = random.randint(20000, 200000)
            the_spliter = message.content.split(' ')
            if len(the_spliter) == 2:
                evil = int(the_spliter[1])
            for x in range(0, length):
                if random.randint(0, evil) != 0: # 60000, 40000
                    output.append(read[x])
                else:
                    output.append(random.randint(0,255))
            dest_file = f'ferrari_{time.time()}.webm'
            converted_file = dest_file + ".mp4"
            with open(dest_file, 'wb') as dst:
                dst.write(output)
            retcode = subprocess.call(f"ffmpeg -i {dest_file} -preset fast "
                                      f"-b:a {random.randint(35,300)}k "
                                      f"-b:v {random.randint(800,2000)}k "
                                      f"{converted_file}", shell=True)
            if retcode < 0:
                print("Child was terminated by signal", -retcode, file=sys.stderr)
                await message.channel.send('a skill issue happened,,, ohno ,,,,')
            else:
                print("Child returned", retcode, file=sys.stderr)
            file = discord.File(converted_file, filename=converted_file)
            await message.channel.send(file=file)
            print("woo yeah woo yeah")
        """
        if self.client.user.mentioned_in(message) or message.content.startswith("!tye"):
            await message.channel.typing()

            channel_msg_str = message.content.replace("!tye ", "").replace("!tye", "")
            prompt = "---\n" + channel_msg_str + "\n"
            print("prompt:\n" + prompt)

            temperature = random.uniform(0.6, 1.0)  # 0.1,1
            temperature_increase = 1.05
            output = ""

            while not output.strip():
                output = tye_ai.generate_one(
                    temperature=temperature,
                    prompt=prompt,
                    repetition_penalty=1.19,
                    max_length=128,
                )
                print(f"temperature: {temperature}")
                print(f"output: {output}")
                temperature_increase = pow(temperature_increase, 1.1)
                temperature += temperature_increase * 0.1

            output = output.split("---\n")[1]
            output = output.strip(channel_msg_str)

            await message.channel.send(output, allowed_mentions=allowedMentions)


tye_bot = TyeBot(tye)
