from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TOKEN, CHANNEL_USERNAME, PDF_PATH
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        chat_member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)

        if chat_member.status in ['member', 'creator', 'administrator']:
            await update.message.reply_text("🎉 Спасибо за подписку! Лови твой PDF-гайд 👇")
            if os.path.exists(PDF_PATH):
                with open(PDF_PATH, "rb") as pdf:
                    await context.bot.send_document(chat_id=user_id, document=pdf)
            else:
                await update.message.reply_text("⚠️ PDF-файл не найден на сервере.")
        else:
            await update.message.reply_text("❗️Сначала подпишись на наш канал: https://t.me/ai_no_code")
    except Exception as e:
        print(f"[ERROR] {e}")
        await update.message.reply_text("⚠️ Произошла ошибка. Попробуй позже.")

if __name__ == '__main__':
    import asyncio
    from telegram.ext import ApplicationBuilder

    async def main():
        app = ApplicationBuilder().token(TOKEN).build()
        await app.bot.delete_webhook()
        app.add_handler(CommandHandler("start", start))
        print("🤖 Бот запущен...")
        await app.run_polling()

    asyncio.run(main())
