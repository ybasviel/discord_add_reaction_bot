import re
import unicodedata
import discord

with open("bot.token") as tokenfile:
    TOKEN = tokenfile.read()

def transform_unicode_emoji(char):

    #絵文字のA(0x1f1e6) - アルファベットのA(0x0041) + 入力する文字
    return chr(0x1f1e6 - 0x0041 + ord(char.upper()))
    

def str_to_reactions(string):

    reactions = []
    for char in  string:
        reactions.append(transform_unicode_emoji(char))

    return reactions


def is_japanese(string):
    for char in string:
        name = unicodedata.name(char) 
        if "CJK UNIFIED" in name or "HIRAGANA" in name or "KATAKANA" in name:
            return True
    return False



client = discord.Client()

@client.event
async def on_ready():
    print('login!')


@client.event
async def on_message(message):

    if message.author.bot:
        return

    if message.content.startswith("!!reaction"):
        array_message = re.split("[ /]" ,message.content)
        msg_channel_id_int = int(array_message[-3])
        msg_id_int = int(array_message[-2])

        if not is_japanese(array_message[-1]):
        
            reactions = str_to_reactions(array_message[-1])
            msg_channel = client.get_channel(msg_channel_id_int)
            msg_id = await msg_channel.fetch_message(msg_id_int)

            for reaction in reactions:
                await msg_id.add_reaction(reaction)

        else:
            await message.channel.send("Error! Use Alphabet Only")


client.run(TOKEN)
