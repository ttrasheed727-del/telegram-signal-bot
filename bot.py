import os
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import WebAppInfo

from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import ContextTypes


TOKEN = os.getenv("BOT_TOKEN", "").strip()
PORT = int(os.getenv("PORT", "10000"))

PUBLIC_URL = os.getenv(
    "PUBLIC_URL",
    os.getenv("RENDER_EXTERNAL_URL", "")
).strip().rstrip("/")


if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

if not PUBLIC_URL:
    raise RuntimeError("PUBLIC_URL is missing")


class WebHandler(SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        pass


def run_web_server():

    server = ThreadingHTTPServer(
        ("0.0.0.0", PORT),
        WebHandler
    )

    print("Web server running on port", PORT)

    server.serve_forever()


def home_keyboard():

    buttons = [
        [
            InlineKeyboardButton(
                "⚡ Advance Signal",
                callback_data="advance"
            )
        ],
        [
            InlineKeyboardButton(
                "📷 Direct Live Scan",
                web_app=WebAppInfo(
                    url=PUBLIC_URL + "/camera.html"
                )
            )
        ]
    ]

    return InlineKeyboardMarkup(buttons)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["signal_set"] = 0

    await update.message.reply_text(
        "⚡ OLYMP TRADE SIGNAL\n\n"
        "Select an option 👇",
        reply_markup=home_keyboard()
    )


async def advance_signal(query, context):

    set_number = context.user_data.get("signal_set", 0) + 1

    context.user_data["signal_set"] = set_number

    buttons = [
        [
            InlineKeyboardButton(
                "🔄 Next Set",
                callback_data="advance"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Home",
                callback_data="home"
            )
        ]
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    message = (
        "⚡ ADVANCE SIGNAL — SET "
        + str(set_number)
        + "\n\n"
        + "Searching for valid setups...\n\n"
        + "Maximum 10 signals per set.\n"
        + "No random signals."
    )

    await query.edit_message_text(
        message,
        reply_markup=keyboard
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if query.data == "advance":

        await advance_signal(
            query,
            context
        )

    elif query.data == "home":

        await query.edit_message_text(
            "⚡ OLYMP TRADE SIGNAL\n\n"
            "Select an option 👇",
            reply_markup=home_keyboard()
        )


def main():

    web_thread = threading.Thread(
        target=run_web_server,
        daemon=True
    )

    web_thread.start()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    print("Olymp Trade Signal Bot running...")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
