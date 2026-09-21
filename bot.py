import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = "".join(os.getenv("BOT_TOKEN", "").split())

# Country / timezone options
TIMEZONES = {
    "india": ("🇮🇳 India", "Asia/Kolkata"),
    "saudi": ("🇸🇦 Saudi Arabia", "Asia/Riyadh"),
    "uae": ("🇦🇪 UAE", "Asia/Dubai"),
    "qatar": ("🇶🇦 Qatar", "Asia/Qatar"),
    "kuwait": ("🇰🇼 Kuwait", "Asia/Kuwait"),
    "bahrain": ("🇧🇭 Bahrain", "Asia/Bahrain"),
    "oman": ("🇴🇲 Oman", "Asia/Muscat"),
    "pakistan": ("🇵🇰 Pakistan", "Asia/Karachi"),
    "bangladesh": ("🇧🇩 Bangladesh", "Asia/Dhaka"),
    "srilanka": ("🇱🇰 Sri Lanka", "Asia/Colombo"),
    "malaysia": ("🇲🇾 Malaysia", "Asia/Kuala_Lumpur"),
    "singapore": ("🇸🇬 Singapore", "Asia/Singapore"),
    "indonesia": ("🇮🇩 Indonesia", "Asia/Jakarta"),
    "uk": ("🇬🇧 United Kingdom", "Europe/London"),
    "usa": ("🇺🇸 USA - New York", "America/New_York"),
}

# Olymp Trade OTC assets
ASSETS = [
    "NZD/USD OTC",
    "AUD/CAD OTC",
    "AUD/CHF OTC",
    "AUD/JPY OTC",
    "AUD/NZD OTC",
    "CAD/CHF OTC",
    "CAD/JPY OTC",
    "CHF/JPY OTC",
    "EUR/AUD OTC",
    "EUR/CAD OTC",
    "EUR/CHF OTC",
    "EUR/GBP OTC",
    "EUR/JPY OTC",
    "EUR/NZD OTC",
    "EUR/USD OTC",
    "GBP/AUD OTC",
    "GBP/CAD OTC",
    "GBP/CHF OTC",
    "GBP/JPY OTC",
    "GBP/NZD OTC",
    "GBP/USD OTC",
    "NZD/CAD OTC",
    "NZD/CHF OTC",
    "NZD/JPY OTC",
    "USD/CAD OTC",
    "USD/CHF OTC",
    "AUD/USD OTC",
    "USD/JPY OTC",
    "BNB OTC",
    "Bitcoin OTC",
    "Dogecoin OTC",
    "Ethereum OTC",
    "Litecoin OTC",
    "PEPE OTC",
    "Ripple OTC",
    "Solana OTC",
    "Gold OTC",
    "Silver OTC",
]


def country_keyboard():
    rows = []
    items = list(TIMEZONES.items())

    for i in range(0, len(items), 2):
        row = []

        key1, value1 = items[i]
        row.append(
            InlineKeyboardButton(
                value1[0],
                callback_data=f"tz:{key1}"
            )
        )

        if i + 1 < len(items):
            key2, value2 = items[i + 1]
            row.append(
                InlineKeyboardButton(
                    value2[0],
                    callback_data=f"tz:{key2}"
                )
            )

        rows.append(row)

    return InlineKeyboardMarkup(rows)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 OTC AI\n\n"
        "📊 Olymp Trade OTC\n"
        "⏱ 1 Minute Mode\n"
        "🌍 UTC Auto Time Converter\n"
        "🚫 No Martingale\n\n"
        "👇 Select your country/timezone:"
    )

    await update.message.reply_text(
        text,
        reply_markup=country_keyboard()
    )


async def timezone_selected(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    key = query.data.split(":", 1)[1]

    if key not in TIMEZONES:
        await query.edit_message_text("❌ Invalid timezone.")
        return

    country_name, zone_name = TIMEZONES[key]

    context.user_data["timezone"] = zone_name
    context.user_data["country"] = country_name

    now_utc = datetime.now(timezone.utc)
    local_time = now_utc.astimezone(ZoneInfo(zone_name))

    text = (
        "✅ Timezone Selected\n\n"
        f"{country_name}\n"
        f"🌐 UTC: {now_utc.strftime('%H:%M:%S')}\n"
        f"🕐 Local: {local_time.strftime('%H:%M:%S')}\n\n"
        "OTC AI is ready."
    )

    await query.edit_message_text(text)


async def time_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    zone_name = context.user_data.get("timezone")

    if not zone_name:
        await update.message.reply_text(
            "🌍 First select your country:",
            reply_markup=country_keyboard()
        )
        return

    country = context.user_data.get("country", "")
    now_utc = datetime.now(timezone.utc)
    local_time = now_utc.astimezone(ZoneInfo(zone_name))

    await update.message.reply_text(
        f"🌐 UTC: {now_utc.strftime('%H:%M:%S')}\n"
        f"{country}: {local_time.strftime('%H:%M:%S')}"
    )


async def assets_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    lines = ["📊 OTC AI ASSETS\n"]

    for number, asset in enumerate(ASSETS, start=1):
        lines.append(f"{number}. {asset}")

    await update.message.reply_text("\n".join(lines))


async def status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🟢 OTC AI ONLINE\n\n"
        "⏱ Mode: 1 Minute\n"
        "🌐 Master Time: UTC\n"
        "🌍 Local Time: Automatic\n"
        "🚫 Martingale: OFF"
    )


async def signal(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🔎 OTC AI Signal Engine\n\n"
        "⏳ Waiting for confirmed market data...\n\n"
        "UP/DOWN will only be sent after the "
        "market-data analysis engine is connected.\n"
        "Random signals are disabled."
    )


def main():
    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is missing. Add BOT_TOKEN "
            "to your hosting environment variables."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("time", time_command))
    app.add_handler(CommandHandler("assets", assets_command))
    app.add_handler(CommandHandler("signal", signal))

    app.add_handler(
        CallbackQueryHandler(
            timezone_selected,
            pattern=r"^tz:"
        )
    )

    print("OTC AI BOT STARTED")
    app.run_polling()


if __name__ == "__main__":
    main()
