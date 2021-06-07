import discord
from datetime import date
import _csv
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="config")
os.getenv("TOKEN")

client = discord.Client()
print('up and runnig  ')
type_debit = '-'

today = date.today()


def reader(filename):
    with open(filename, "r") as csvfile:
        read_csv = _csv.reader(csvfile)
        for row in read_csv:
            last_line = row
        return last_line


def writer(data, filename):
    with open(filename, "a", newline="", encoding='utf-8') as csvfile:
        file = _csv.writer(csvfile)
        file.writerow(data)


@client.event
async def on_ready():
    print("Le bot est prêt !")


@client.event
async def on_message(message):  # when a new message is detected in the server
    if message.author == client.user:  # don't respond to own message sent by the bot
        return

    if message.content == "!debit":
        await message.channel.send('Combien a été retiré : ')

        msg = await client.wait_for('message')
        debit = msg.content
        await message.channel.send("Tu as retiré :{}€ ".format(msg.content))

        try:
            debit = float(int(debit))
        except:
            debit = float(debit)

        await message.channel.send("Qu'est ce que tu as retiré : ")

        msg = await client.wait_for('message')
        type_debit = msg.content
        await message.channel.send("Tu as retiré :{} ".format(msg.content))

        last_line = reader('data.csv')
        argent_avant_debit = float(last_line[2])
        writer([argent_avant_debit, debit,
                argent_avant_debit-debit, type_debit, today], 'data.csv')
        await message.channel.send('Tu avais {}, tu as dépensé {} de {} il te reste {} le {}'.format(argent_avant_debit, debit,  type_debit, argent_avant_debit-debit, today))

    if message.content == '!argent':
        ligne = reader('data.csv')
        await message.channel.send('Il te reste {}€'.format(ligne[2]))

    if message.content == '!csv':
        await message.channel.send(file=discord.File('data.csv'))

    if message.content == '!help':
        # await message.channel.send('Envoie !debit pour rentrer une nouvelle dépense')
        # await message.channel.send("Envoie !argent pour voir ce qu'il te reste")
        # await message.channel.send("Envoie !csv pour recevoir le csv de toute tes transactions.")

        em = discord.Embed(
            title="Help", description="Liste des commandes principales")
        em.add_field(name="!argent", value="Voir ce qui reste sur le compte")
        em.add_field(
            name="!csv", value="Envoie !csv pour recevoir le csv de toute tes transactions.")
        em.add_field(
            name="!debit", value="Envoie !debit pour rentrer une nouvelle dépense")
        await message.channel.send(embed=em)

client.run('ODUxMTEwNDYxMzQ0OTcyODIw.YLzgYg.x7M_6og1G84rkDGR9KbwmZHuFbA')
