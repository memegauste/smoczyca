# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord, os
import glac, config

client = discord.Client()
fTable = []
allow_permission = ["Szef", "Schizol", "Zastępca"]

def readShitpost():
    del fTable[:]
    for filename in os.listdir("{:s}/shitpost/".format(os.getcwd())):
        file = str.split(filename, ".")
        fTable.append(file[0])

readShitpost()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith(tuple(fTable)):
        cmdBuff = message.content.split(" ")
        cmd = cmdBuff[0]
        fBuffer = open("./shitpost/{:s}.meme".format(cmd), "r+")
        msg = ''
        msg = fBuffer.read()
        await client.send_message(message.channel, msg)

    if message.content.startswith('!checkrole'):
        msg = message.author.top_role
        await client.send_message(message.channel, msg)

    if message.content.startswith('!add'):
        if(message.author.top_role.name in allow_permission):
            msg = message.content.split(" ")
            if(len(msg) > 2):
                fName = msg[1]
                fContent = ' '.join(msg[2:])
                fBuffer = open("./shitpost/{:s}.meme".format(fName), "w+")
                fBuffer.write(fContent)
                await client.send_message(message.channel, ("Added command: {:s}".format(msg[1])))
                fBuffer.close()
                readShitpost()
            else:
                await client.send_message(message.channel, "Three or more words needed!")
        else:
            await client.send_message(message.channel, "No correct permission!")

    if message.content.startswith('!delete'):
        if(message.author.top_role.name in allow_permission):
            msg = message.content.split(" ")
            fName = msg[1]
            os.remove("./shitpost/{:s}.meme".format(fName))
            await client.send_message(message.channel, ("Deleted file!"))
            readShitpost()
        else:
            await client.send_message(message.channel, "No correct permission!")

    if message.content.startswith('!ver'):
        embed = discord.Embed(title="Discord.py version", description=discord.__version__)
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith('!glac'):
        data = glac.read()
        embed = discord.Embed(title="Status glacy", description="Kochajmy glacowiczów, tak szybko umierają.")
        embed.add_field(name="Anioły", value=data["angels"]["progress"], inline=False)
        embed.add_field(name="Demony", value=data["demons"]["progress"], inline=False)
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith('!avatar'):
        if len(message.mentions) > 0:
            for user in message.mentions:
                msg = user.avatar_url
                await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print("Logged in as {:s} as ID: {:s}".format(client.user.name, client.user.id))
    print('------')

client.run(config.returnToken())