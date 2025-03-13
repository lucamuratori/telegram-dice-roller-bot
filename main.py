import logging
import re
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
def d4(n):
    for i in range(n):
        yield random.randint(1, 4)

def d6(n):
    for i in range(n):
        yield random.randint(1, 6)

def d8(n):
    for i in range(n):
        yield random.randint(1, 8)

def d10(n):
    for i in range(n):
        yield random.randint(1, 10)

def d12(n):
    for i in range(n):
        yield random.randint(1, 12)

def d20(n):
    for i in range(n):
        yield random.randint(1, 20)

def d100(n):
    for i in range(n):
        yield random.randint(1, 100)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    match = re.match(r'(\d+)?d(\d+)(h)?(\d)?', ''.join(context.args))
    if match:
        n = int(match.group(1) or 1)
        dice = int(match.group(2))
        if dice == 4:
            mes = list(d4(n))
        elif dice == 6:
            mes = list(d6(n))
        elif dice == 8:
            mes = list(d8(n))
        elif dice == 10:
            mes = list(d10(n))
        elif dice == 12:
            mes = list(d12(n))
        elif dice == 20:
            mes = list(d20(n))
        elif dice == 100:
            mes = list(d100(n))
    
        if match.group(3) == 'h':
            if not match.group(4):
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{mes} = {sum(mes)}')
            elif int(match.group(4)) > n:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Error! The number of dice to keep can't be higher than the number of dice rolled. Try again.")
            elif int(match.group(4)) == n:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{mes} = {sum(mes)}')
            else:
                for _ in range(int(match.group(1)) - int(match.group(4))):
                    mes.remove(min(mes))
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{mes} = {sum(mes)}')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{mes} = {sum(mes)}')
    

if __name__ == '__main__':
    application = ApplicationBuilder().token('TOKEN').build()
    
    start_handler = CommandHandler('start', start)
    roll_handler = CommandHandler('roll', roll)
    


    application.add_handler(start_handler)
    application.add_handler(roll_handler)
    
    application.run_polling()