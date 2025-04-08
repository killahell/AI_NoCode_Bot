from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TOKEN, CHANNEL_USERNAME, PDF_PATH

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        chat_member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)

        if chat_member.status in ['member', 'creator', 'administrator']:
            await update.message.reply_text("🎉 Спасибо за подписку! Лови твой PDF-гайд 👇")
            await context.bot.send_document(chat_id=user_id, document=InputFile(PDF_PATH))
        else:
            await update.message.reply_text("❗️Сначала подпишись на наш канал: https://t.me/ai_no_code")
    except Exception as e:
        print(f"[ERROR] {e}")
        await update.message.reply_text("⚠️ Произошла ошибка. Попробуй позже.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    import asyncio
    async def remove_webhook():
        try:
            await app.bot.delete_webhook()
        except Exception as e:
            print(f"[ERROR webhook] {e}")

    asyncio.run(remove_webhook())

    app.add_handler(CommandHandler("start", start))
    app.run_polling()
