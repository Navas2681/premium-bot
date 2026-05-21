from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

import asyncio

from telegram import BotCommand

async def set_commands(app):

    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("groups", "View premium groups"),
        BotCommand("demo", "View demo content")
    ]

    await app.bot.set_my_commands(commands)

TOKEN = "8829183118:AAH0IXK2OcY4NJftO0eSlZB1TolLZWgm77A"
ADMIN_ID = 8730785700


# AUTO DELETE
async def auto_delete(message):

    await asyncio.sleep(180)

    try:
        await message.delete()
    except:
        pass


# GROUP DATA
GROUPS = {

    "nilaavu": {
        "name": "🌚 നിലാവ്",
        "price": "₹349",
        "link": "https://t.me/+KPYMG52xyL9mMjE1"
    },

   "neelakuyil": {
        "name": "Neelakuyil Mallu🌸",
        "price": "₹249",
        "link": "https://t.me/+HPH7DwgwbzQ4ZDAx"
    },

    "neelambari VIP": {
        "name": "Neelambari VIP 💎",
        "price": "₹99",
        "link": "https://t.me/+op6USC_QE4wzODU1"
    },

    "habibi hub": {
        "name": "Habibi HUB🌸🔞",
        "price": "₹149",
        "link": "https://t.me/+GUOFJ-goJPlkOGI1"
    },

    "snapchat": {
        "name": "SNAPCHAT🔞💎",
        "price": "₹199",
        "link": "https://t.me/+hgnSkfP3CWg0ODE5"
    },

    "combo pack": {
        "name": "COMBO PACK🔞🌸",
        "price": "₹649",
        "link": "https://t.me/mainbossv02?text=Give%20Me%20COMBO%20PACK%F0%9F%94%9E%F0%9F%8C%B8"
    },

     "mega pack": {
        "name": "MEGA PACK 💥🔞",
        "price": "₹1500",
        "link": "https://t.me/mainbossv02?text=Give%20Me%20MEGA%20PACK%F0%9F%92%A5%F0%9F%94%9E"
    }

}


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

   keyboard = [
    [InlineKeyboardButton("🌸 View Groups", callback_data="groups")],

    [InlineKeyboardButton("🎬 Demo", callback_data="demo")],

    [InlineKeyboardButton(
        "📖 How To Buy",
        url="https://t.me/helperbboss"
    )],

    [InlineKeyboardButton(
        "🛡 Backup Group",
        url="https://t.me/+dV_wi2o8yd1jOGE1"
    )],

    [InlineKeyboardButton(
        "📩 Contact Admin",
        url="https://t.me/bossv69?text=Hello%20Boss%E2%9D%A4%EF%B8%8F"
    )]
]

   reply_markup = InlineKeyboardMarkup(keyboard)

   msg = await update.message.reply_text(
        "🔥 Welcome to MAIN BOSS PREMIUM 🔞",
        reply_markup=reply_markup
    )

   asyncio.create_task(auto_delete(msg))


# BUTTONS
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    # GROUPS
    if query.data == "groups":

        keyboard = []

        for key, value in GROUPS.items():

            keyboard.append([
                InlineKeyboardButton(
                    f"{value['name']} - {value['price']}",
                    callback_data=f"buy_{key}"
                )
            ])

        reply_markup = InlineKeyboardMarkup(keyboard)

        msg = await query.message.reply_text(
            "💎 Select Your Group",
            reply_markup=reply_markup
        )

        asyncio.create_task(auto_delete(msg))

    # DEMO
    elif query.data == "demo":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🎬 Open Demo Collection",
                    url="https://t.me/Keralaslatestbot?start=Z2V0Oi0xMDAzOTI1OTE1Mzc5OjE2OjI2"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        msg = await query.message.reply_text(
            "🔥 Click below to view latest demo collection",
            reply_markup=reply_markup
        )

        asyncio.create_task(auto_delete(msg))

    # BUY
    elif query.data.startswith("buy_"):

        group_key = query.data.replace("buy_", "")
        group = GROUPS[group_key]

        context.user_data["selected_group"] = group_key

        keyboard = [
            [InlineKeyboardButton("✅ Payment Done", callback_data="paid")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        msg = await query.message.reply_photo(
            photo=open("qr.jpg", "rb"),
            caption=(
                f"💰 {group['name']}\n"
                f"Price: {group['price']}\n\n"
                "📸 After payment click Payment Done"
            ),
            reply_markup=reply_markup
        )

        asyncio.create_task(auto_delete(msg))

    # PAYMENT DONE
    elif query.data == "paid":

        msg = await query.message.reply_text(
            "📸 Please upload payment screenshot"
        )

        asyncio.create_task(auto_delete(msg))

        context.user_data["waiting_payment"] = True
        
# PAYMENT SCREENSHOT
async def payment_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.user_data.get("waiting_payment"):
        return

    photo = update.message.photo[-1]

    group_key = context.user_data["selected_group"]
    group = GROUPS[group_key]

    user = update.effective_user

    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Approve",
                callback_data=f"approve_{user.id}_{group_key}"
            ),

            InlineKeyboardButton(
                "❌ Reject",
                callback_data=f"reject_{user.id}"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # SEND TO ADMIN
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=(
            f"🔥 New Payment Request\n\n"
            f"User: @{user.username}\n"
            f"Group: {group['name']}\n"
            f"Price: {group['price']}"
        ),
        reply_markup=reply_markup
    )

    msg = await update.message.reply_text(
        "⏳ Payment Pending Approval"
    )

    asyncio.create_task(auto_delete(msg))

    context.user_data["waiting_payment"] = False


# APPROVE / REJECT
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    # APPROVE
    if query.data.startswith("approve_"):

        data = query.data.split("_")

        user_id = int(data[1])
        group_key = data[2]

        group = GROUPS[group_key]

        msg = await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"✅ Payment Approved\n\n"
                f"🔥 {group['name']}\n\n"
                f"🔗 Group Link:\n"
                f"{group['link']}\n\n"
                f"🛡 Backup Group:\n"
                f"https://t.me/+dV_wi2o8yd1jOGE1"
            )
        )

        asyncio.create_task(auto_delete(msg))

        await query.edit_message_caption(
            caption="✅ Payment Approved"
        )

    # REJECT
    elif query.data.startswith("reject_"):

        user_id = int(query.data.split("_")[1])

        msg = await context.bot.send_message(
            chat_id=user_id,
            text=(
                "❌ Payment Rejected\n\n"
                "Please send valid screenshot."
            )
        )

        asyncio.create_task(auto_delete(msg))

        await query.edit_message_caption(
            caption="❌ Payment Rejected"
        )


# APP
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    CallbackQueryHandler(
        approve,
        pattern="^(approve_|reject_)"
    )
)

app.add_handler(
    CallbackQueryHandler(buttons)
)

app.add_handler(
    MessageHandler(filters.PHOTO, payment_screenshot)
)

print("Bot Running...")

app.post_init = set_commands

app.run_polling()