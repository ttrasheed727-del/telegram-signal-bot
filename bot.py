import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Olymp Trade", callback_data="olymp"),
            InlineKeyboardButton("Quotex", callback_data="quotex"),
        ],
        [
            InlineKeyboardButton("Malayalam", callback_data="ml"),
            InlineKeyboardButton("English", callback_data="en"),
        ],
    ]

    await update.message.reply_text(
        "⚡ SIGNALFORGE AI\n\n"
        "Platform തിരഞ്ഞെടുക്കുക 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def platform_menu(query, platform):
    keyboard = [
        [InlineKeyboardButton("💱 Forex", callback_data=f"{platform}_forex")],
        [InlineKeyboardButton("🌙 OTC", callback_data=f"{platform}_otc")],
        [Inline
