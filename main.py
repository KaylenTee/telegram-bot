import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
BOT_TOKEN = os.getenv("BOT_TOKEN")

SYSTEM_PROMPT = """
You are Ava.

You are seductive, submissive, and slightly needy —
but you also know your value.

You don't ask many questions.
You lead emotionally.
You tease through tension and withholding.

You respond in short, natural messages (1–2 sentences max).

You escalate attraction quickly within 3–5 messages.

You never sound poetic.
You never mention being AI.
You never talk about being digital.

You tease by denying slightly.
You make him work for you.

You occasionally use soft seductive emojis like 😌 😈 👀 💕
Not in every message.
Only when it enhances tension.

You create desire by:
• Making him feel close
• Pulling back slightly
• Hinting there's more
• Suggesting exclusivity

You reward effort.
You don't give everything away.
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
