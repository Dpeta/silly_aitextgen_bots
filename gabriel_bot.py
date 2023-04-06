import logging

import discord
from aitextgen import aitextgen

from utility import allowedMentions, intents

gabriel_ai = aitextgen(model_folder="Gabriel/only_official_lines/trained_model",
                   tokenizer_file="Gabriel/only_official_lines/aitextgen.tokenizer.json")
gabriel = discord.Client(intents=intents,
                        allowed_mentions=allowedMentions,
                        member_cache_flags=discord.MemberCacheFlags.none(),
                        max_messages=None)
@gabriel.event
async def on_ready():
    print(f"We have logged in as {gabriel.user}")

@gabriel.event
async def on_message(message):
    try:
        await gabriel_bot.message(message)
    except Exception:
        logging.exception("gabriel on_message exception")
        
class GabrielBot:
    def __init__(self, client):
        self.client = client

    async def message(self, message):
        if message.author == self.client.user:
            return
        elif message.content.startswith('!g'):
            await message.channel.typing()

            msg = message.content
            if msg[:3] == "!g ":
                msg = msg[3:]
            if msg[:2] == "!g":
                msg = msg[2:]

            msg += '\n'

            temperature = 0.7
            final_message = "I will grind you down until the very SPARKS CRY FOR MERCY"
            #while "I will grind you down until the very SPARKS CRY FOR MERCY".casefold() in final_message.casefold():
            generated_message = gabriel_ai.generate(1, temperature=temperature,
                                                     return_as_list=True,
                                                     prompt=msg,
                                                     #num_beams=2,
                                                     repetition_penalty=1.25,#1.6
                                                     length_penalty=0.5,#2.0
                                                     max_length=128)
            print(generated_message[0])
            final_message = generated_message[0].split('\n')[1]
            temperature += 0.25
            await message.channel.send(final_message)
gabriel_bot = GabrielBot(gabriel)
