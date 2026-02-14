async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # ========= PHOTO PROOF HANDLER =========
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

    # ========= SAFE TEXT CHECK =========
    if not update.message.text:
        return

    user_message = update.message.text.lower()

    # ========= USER STATE SETUP =========
    if user_id not in user_states:
        user_states[user_id] = {
            "messages": 0,
            "buy_attempts": 0,
            "paid_unlock": False
        }

    user_states[user_id]["messages"] += 1

    escalation_words = [
        "see", "show", "body", "pic", "photo",
        "naughty", "private", "more", "content"
    ]

    # ========= ESCALATION SYSTEM =========
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

        if stage >= 3:
            await update.message.reply_photo(
                photo=open("blur.jpg", "rb"),
                caption="If you’re serious… unlock me 😌",
                has_spoiler=True
            )
            return

    # ========= NORMAL AI RESPONSE =========
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
