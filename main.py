import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

user_states = {}

ESCALATION_KEYWORDS = [
    "see", "show", "body", "pic", "photo", "naughty",
    "private", "more", "tease", "prove", "deserve"
]


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
    user_id = update.effective_user.id

    # If user sends screenshot proof (photo)
    if update.message.photo:
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

    # Safe text handling (only if message is text)
    if not update.message.text:
        return

    user_message = update.message.text.lower()


    if user_id not in user_states:
    user_states[user_id] = {
        "messages": 0,
        "buy_attempts": 0,
        "paid_unlock": False
    }

    user_states[user_id]["messages"] += 1

    # Words that trigger escalation
    escalation_words = [
        "see", "show", "body", "pic", "photo",
        "naughty", "private", "more", "content"
    ]

    if any(word in user_message for word in escalation_words):

        user_states[user_id]["buy_attempts"] += 1

        stage = user_states[user_id]["buy_attempts"]

        if stage == 1:
            await update.message.reply_text(
                "Not so fast… not everyone gets that side of me 😌"
            )
            return

        if stage == 2:
    await update.message.reply_text(
        "If you're serious… I just dropped something in my channel 😌\n\n"
        "Unlock it and send me a screenshot after 💕"
    )
    return


        if stage == 3:
    await update.message.reply_photo(
        photo=open("blur.jpg", "rb"),
        caption="If you’re serious… unlock me 😌",
        has_spoiler=True
    )
    return

if user_states[user_id].get("vip_sent"):
    await update.message.reply_text(
        "I’ll be waiting for you there… don’t make me wait too long 😌"
    )
    return


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
        temperature=0.95
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
