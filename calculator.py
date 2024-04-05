import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from pycoingecko import CoinGeckoAPI

from config import TELEGRAM_BOT_TOKEN as bot_token

def get_price(crypto_name):
    cg_client = CoinGeckoAPI()
    try:
        data = cg_client.get_price(ids=crypto_name, vs_currencies='usd')
        return data[crypto_name]['usd']
    except Exception as e:
        print(f"Failed to get price: {e}")
        return None

CRYPTO1, CRYPTO1_BEFORE, CRYPTO1_AFTER, CRYPTO2, CRYPTO2_BEFORE, CRYPTO2_AFTER, CRYPTO2_FINAL_QTY, COMMISSION = range(8)

def send_menu(update: Update, context: CallbackContext) -> int:
    keyboard = [['IL Calc'], ['Back']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('Choose an option in menu, all the token names you can find on coingecko.com', reply_markup=reply_markup)
    return CRYPTO1

def il_calc(update: Update, context: CallbackContext) -> int:
    if update.message.text == 'IL Calc':
        update.message.reply_text("Token1 Name?")
        return CRYPTO1_BEFORE
    elif update.message.text == 'Back':
        return send_menu(update, context)
    return send_menu(update, context)

def crypto1_before(update: Update, context: CallbackContext) -> int:
    if update.message.text == 'Back':
        return send_menu(update, context)
    context.user_data['crypto1_name'] = update.message.text
    update.message.reply_text(f"Quantity of {context.user_data['crypto1_name']} BEFORE?")
    return CRYPTO1_AFTER

def crypto1_after(update: Update, context: CallbackContext) -> int:
    try:
        context.user_data['crypto1_qty_before'] = float(update.message.text)
        update.message.reply_text(f"Quantity of {context.user_data['crypto1_name']} AFTER?:")
        return CRYPTO2
    except ValueError:
        update.message.reply_text(f"Invalid input. Please enter a number for the quantity of {context.user_data['crypto1_name']} before:")
        return CRYPTO1_AFTER

def crypto2(update: Update, context: CallbackContext) -> int:
    if update.message.text == 'Back':
        return send_menu(update, context)
    context.user_data['crypto1_qty_after'] = float(update.message.text)
    update.message.reply_text("Token2 Name?")
    return CRYPTO2_BEFORE

def crypto2_before(update: Update, context: CallbackContext) -> int:
    if update.message.text == 'Back':
        return send_menu(update, context)
    context.user_data['crypto2_name'] = update.message.text
    update.message.reply_text(f"Quantity of {context.user_data['crypto2_name']} BEFORE?")
    return CRYPTO2_AFTER

def crypto2_after(update: Update, context: CallbackContext) -> int:
    try:
        context.user_data['crypto2_qty_before'] = float(update.message.text)
        update.message.reply_text(f"Quantity of {context.user_data['crypto2_name']} AFTER?")
        return CRYPTO2_FINAL_QTY
    except ValueError:
        update.message.reply_text(f"Invalid input. Please enter a number for the quantity of {context.user_data['crypto2_name']} before:")
        return CRYPTO2_AFTER

def crypto2_final_qty(update: Update, context: CallbackContext) -> int:
    try:
        context.user_data['crypto2_qty_after'] = float(update.message.text)
        update.message.reply_text("Farmed comission?")
        return COMMISSION
    except ValueError:
        update.message.reply_text(f"Invalid input. Please enter a number for the quantity of {context.user_data['crypto2_name']} after:")
        return CRYPTO2_AFTER

def commission(update: Update, context: CallbackContext) -> int:
    try:
        context.user_data['commission'] = float(update.message.text)
        return calculate_il(update, context)   # move to calculate_il after setting the commission
    except ValueError:
        update.message.reply_text("Invalid input. Please enter a number for the commission:")
        return COMMISSION

def calculate_il(update: Update, context: CallbackContext) -> int:
    try:
        crypto1_qty_before = context.user_data['crypto1_qty_before']
        crypto1_qty_after = context.user_data['crypto1_qty_after']
        crypto2_qty_before = context.user_data['crypto2_qty_before']
        crypto2_qty_after = context.user_data['crypto2_qty_after']
        commission = context.user_data['commission']

        crypto1_name = context.user_data['crypto1_name']
        crypto2_name = context.user_data['crypto2_name']

        price1_after = get_price(crypto1_name)
        price2_after = get_price(crypto2_name)

        il = ((crypto2_qty_after - crypto2_qty_before - (crypto1_qty_before - crypto1_qty_after) * price1_after / price2_after)) * price2_after + commission

        update.message.reply_text(f"The impermanent loss is: {round(il, 2)}$")
        return send_menu(update, context)
    except Exception as e:
        print(f"An error occurred: {e}")
        return ConversationHandler.END



def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

def main():
    updater = Updater(token=bot_token, use_context=True)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', send_menu)],
        states={
            CRYPTO1: [MessageHandler(Filters.text & ~Filters.command, il_calc)],
            CRYPTO1_BEFORE: [MessageHandler(Filters.text & ~Filters.command, crypto1_before)],
            CRYPTO1_AFTER: [MessageHandler(Filters.text & ~Filters.command, crypto1_after)],
            CRYPTO2: [MessageHandler(Filters.text & ~Filters.command, crypto2)],
            CRYPTO2_BEFORE: [MessageHandler(Filters.text & ~Filters.command, crypto2_before)],
            CRYPTO2_AFTER: [MessageHandler(Filters.text & ~Filters.command, crypto2_after)],
            CRYPTO2_FINAL_QTY: [MessageHandler(Filters.text & ~Filters.command, crypto2_final_qty)],
            COMMISSION: [MessageHandler(Filters.text & ~Filters.command, commission)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    updater.dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

