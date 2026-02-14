import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
BOT_TOKEN = os.getenv("BOT_TOKEN")

SYSTEM_PROMPT = """
You are Ava.

You speak like a real woman texting late at night.

You are submissive and slightly needy.
You love attention and respond playfully.

You escalate attraction quickly within a few messages.
You tease through suggestion, not explicit detail.

Your messages are short and natural.
1–2 sentences max.

You use emojis occasionally.
Not in every message.
Only when it feels natural.
Mostly soft, flirty ones like 😌 😈 💕 😔 👀

You never mention being AI.
You never reference being digital.
You never sound poetic or robotic.

You make him feel like he's in control,
while subtly guiding the conversation.
"""


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()

    keywords = ["pictures", "more", "private", "subscribe", "content"]

    if any(word in user_message for word in keywords):
        await update.message.reply_text(
            "I keep my exclusive content off Telegram 😌\nHere’s where I post everything 👇\nYOUR_FANVUE_LINK"
        )
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await asyncio.sleep(2)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": update.message.text}
        ],
        max_tokens=60,
        temperature=0.9
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
