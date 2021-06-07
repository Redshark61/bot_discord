import discord
from datetime import date
import _csv


client = discord.Client()
print('up and runnig  ')
type_debit = '-'

today = date.today()
bank = [['Avant retrait', 'Débit', 'Après retrait',
         'Type de retrait', 'Date de retrait'], [100, 0, 100, type_debit, today]]


def writer(data, filename):
    with open(filename, "w", newline="", encoding='utf-8') as csvfile:
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

        argent_avant_debit = float(bank[-1][2])
        bank.append([argent_avant_debit, debit,
                    argent_avant_debit-debit, type_debit, today])
        await message.channel.send('Tu avais {}, tu as dépensé {} de {} il te reste {} le {}'.format(argent_avant_debit, debit,  type_debit, argent_avant_debit-debit, today))
        writer([argent_avant_debit, debit,
                argent_avant_debit-debit, type_debit, today], 'data.csv')

    if message.content == '!argent':
        await message.channel.send('Il te reste {}€'.format(bank[-1][2]))

    if message.content == '!help':
        await message.channel.send('Envoie !debit pour rentrer une nouvelle dépense')
        await message.channel.send("Envoie !argent pour voir ce qu'il te reste")

client.run('token')
