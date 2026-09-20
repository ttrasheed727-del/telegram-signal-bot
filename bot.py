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


def home_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Olymp Trade", callback_data="olymp"),
                InlineKeyboardButton("Quotex", callback_data="quotex"),
            ],
            [
                InlineKeyboardButton("Malayalam", callback_data="lang_ml"),
                InlineKeyboardButton("English", callback_data="lang_en"),
            ],
        ]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚡ SIGNALFORGE AI\n\n"
        "Platform തിരഞ്ഞെടുക്കുക 👇",
        reply_markup=home_keyboard(),
    )


async def platform_menu(query, platform):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💱 Forex", callback_data=f"{platform}_forex")],
            [InlineKeyboardButton("🌙 OTC", callback_data=f"{platform}_otc")],
            [InlineKeyboardButton("🥇 Gold", callback_data=f"{platform}_gold")],
            [InlineKeyboardButton("₿ Crypto", callback_data=f"{platform}_crypto")],
            [InlineKeyboardButton("📊 Indices", callback_data=f"{platform}_indices")],
            [InlineKeyboardButton("⬅️ Back", callback_data="home")],
        ]
    )

    name = "Olymp Trade" if platform == "olymp" else "Quotex"

    await query.edit_message_text(
        f"⚡ SIGNALFORGE AI\n\n{name}\n\nCategory തിരഞ്ഞെടുക്കുക 👇",
        reply_markup=keyboard,
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "olymp":
        await platform_menu(query, "olymp")

    elif data == "quotex":
        await platform_menu(query, "quotex")

    elif data == "home":
        await query.edit_message_text(
            "⚡ SIGNALFORGE AI\n\n"
            "Platform തിരഞ്ഞെടുക്കുക 👇",
            reply_markup=home_keyboard(),
        )

    elif data == "lang_ml":
        await query.edit_message_text(
            "⚡ SIGNALFORGE AI\n\n"
            "ഭാഷ: മലയാളം ✅\n\n"
            "Platform തിരഞ്ഞെടുക്കുക 👇",
            reply_markup=home_keyboard(),
        )

    elif data == "lang_en":
        await query.edit_message_text(
            "⚡ SIGNALFORGE AI\n\n"
            "Language: English ✅\n\n"
            "Choose a platform 👇",
            reply_markup=home_keyboard(),
        )

    else:
        await query.edit_message_text(
            "⚡ SIGNALFORGE AI\n\n"
            f"Selected: {data}\n\n"
            "Asset list will be added in the next update.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ Back", callback_data="home")]]
            ),
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("SIGNALFORGE AI bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
