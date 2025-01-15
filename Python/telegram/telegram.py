from telegram import *
from telegram.ext import *

token = "6097784508:AAG4BNhkMFMJYE9dB3g6QPi_HxQAzCqlrL8"

bot = Bot(token)
#print(bot.get_me())
updater = Updater(token, use_context=True)

dispatcher= updater.dispatcher


def test_func(update:Update, context:CallbackContext):
    bot.send_message(
        chat_id = update.effective_chat.id,
        text ="tutorial link : https://youtu.be/Tm5u97I7OrM",
    )
start_value = CommandHandler('motion_detection',test_func)

dispatcher.add_handler(start_value)

updater.start_polling()