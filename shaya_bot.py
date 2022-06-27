from os import getenv
from dotenv import load_dotenv
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
import telegram
import telegram.ext as tgram_e
import pandas_datareader as pdr


def start(update: Update, context: tgram_e.CallbackContext):
    name = update.message.chat.first_name
    start_text = f'Hello {name}! Welcome to Shaya\'s Bot!\n\nPress "/" or choose a command from the menu.'

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=start_text,
    )


def help_command(update: Update, context: tgram_e.CallbackContext):
    help_text = """
    The following commands are available:

    /start -> Welcome Message
    /help -> This message
    /content -> Info about Shaya
    /contact -> Contact Info
    /stock -> Check on stocks
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=help_text,
    )


def content(update: Update, context: tgram_e.CallbackContext):
    content_text = """
    Shaya was born in October 1994.
He plays the viola in the IPO.

This is his first personal Telegram Bot.
He will use it for his learning.
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=content_text,
    )


def contact(update: Update, context: tgram_e.CallbackContext):
    contact_text = """
    You can contact Shaya on Telegram\n(and WhatsApp... shhh)
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=contact_text,
    )


def stock(update: Update, context: tgram_e.CallbackContext):
    TICKERS = {"S&P500": "^GSPC", "NASDAQ": "^IXIC", "Tesla": "TSLA", "Apple": "AAPL"}
    INLINE_BUTTONS = [
        [InlineKeyboardButton(text=stock, callback_data=stock)]
        for stock in TICKERS.keys()
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Choose a stock:",
        reply_markup=InlineKeyboardMarkup(INLINE_BUTTONS),
    )


def stock_checker(update: Update, context: tgram_e.CallbackContext):
    TICKERS = {"S&P500": "^GSPC", "NASDAQ": "^IXIC", "Tesla": "TSLA", "Apple": "AAPL"}
    stock_name = update.callback_query.data
    ticker = TICKERS[stock_name]
    data = pdr.DataReader(ticker, "yahoo")
    price = data.iloc[-1]["Close"]
    update.callback_query.answer()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"The current price of {stock_name} is {price:.2f}$.",
    )


def add_handlers(disp):
    disp.add_handler(tgram_e.CommandHandler("start", start))
    disp.add_handler(tgram_e.CommandHandler("help", help_command))
    disp.add_handler(tgram_e.CommandHandler("content", content))
    disp.add_handler(tgram_e.CommandHandler("contact", contact))
    disp.add_handler(tgram_e.CommandHandler("stock", stock))
    disp.add_handler(tgram_e.CallbackQueryHandler(stock_checker))


if __name__ == "__main__":
    load_dotenv()
    BOT_KEY = getenv("KEY")
    updater = tgram_e.Updater(BOT_KEY, use_context=True)
    disp = updater.dispatcher
    add_handlers(updater.dispatcher)

    updater.start_polling()
    updater.idle()
