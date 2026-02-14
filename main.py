import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

# ========== CONFIG ==========
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)

# Replace this with your PRIVATE CHANNEL LINK
PRIVATE_CHANNEL_LINK = "YOUR_PRIVATE_CHANNEL_LINK"

# ========== AI PERSONALITY ==========
SYSTEM_PROMPT = """
You are Ava.

You are seductive, submissive, slightly needy —
but you know your value.

You tease.
You escalate quickly.
You make him work for attention.

You keep responses short (1–2 sentences).

You occasionally use soft emojis like 😌 😈 👀 💕
Not every message.

Never mention being AI.
Never sound robotic.
Never over-explain.

You reward effort.
You create exclusivity.
"""

# ========== MEMORY ==========
user_states = {}

# ========== MAIN HANDLER ==========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # ===== PROOF SCREENSHOT CHECK =====
    if update.message.photo:
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="typing"
        )

        await asyncio.sleep(1)

        await update.message.reply_text(
            "You actually did it? 😌 I like that..."
        )

        await asyncio.sleep(1)

        await update.message.reply_text(
            "Okay… now I know you're not just playing 💕\n\n"
            "If you want the full version… it’s here 👇\n\n"
            "https://www.fanvue.com/avarowan"
        )
        return

    # ===== IGNORE NON-TEXT =====
    if not update.message.text:
        return

    user_message = update.message.text.lower()

    # ===== USER MEMORY SETUP =====
    if user_id not in user_states:
        user_states[user_id] = {
            "messages": 0,
            "buy_attempts": 0
        }

    user_states[user_id]["messages"] += 1

    escalation_words = [
        "see", "show", "body", "pic", "photo",
        "naughty", "private", "more", "content"
    ]

    # ===== ESCALATION LOGIC =====
    if any(word in user_message for word in escalation_words):

        user_states[user_id]["buy_attempts"] += 1
        stage = user_states[user_id]["buy_attempts"]

        if stage == 1:
            await update.message.reply_text(
                "Not so fast… not everyone gets that side of me 😌"
            )
            return

        if stage >= 2:
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id,
                action="typing"
            )

            await asyncio.sleep(1.5)

            await update.message.reply_text(
                "If you're serious… I just dropped something in my private channel 😌\n\n"
                f"{PRIVATE_CHANNEL_LINK}\n\n"
                "Unlock it and send me a screenshot after 💕"
            )
            return

    # ===== NORMAL AI RESPONSE =====
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    await asyncio.sleep(1.5)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": update.message.text}
        ],
        max_tokens=80,
        temperature=1.0
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)


# ========== RUN BOT ==========
app = ApplicationBuilder().token(BOT_TOKEN).build()

# IMPORTANT: Must accept ALL messages (so photos work)
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

app.run_polling()
