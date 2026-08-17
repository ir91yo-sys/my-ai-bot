import os
import logging
import time
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получаем ключи из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Инициализация клиента Groq (совместим с OpenAI)
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Словарь для хранения истории переписки (в оперативной памяти)
conversation_histories = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    conversation_histories[chat_id] = [
        {"role": "system", "content": "Ты мой личный друг и собеседник. Общайся со мной тепло, дружелюбно и по-человечески. Отвечай развернуто, но без лишнего официоза, как в живом диалоге."}
    ]
    await context.bot.send_message(
        chat_id=chat_id, 
        text="Привет! Я твой персональный собеседник. Можем болтать о чем угодно. Если захочешь начать диалог заново, просто напиши /clear"
    )

# Команда /clear
async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    conversation_histories[chat_id] = [
        {"role": "system", "content": "Ты мой личный друг и собеседник. Общайся со мной тепло, дружелюбно и по-человечески. Отвечай развернуто, но без лишнего официоза, как в живом диалоге."}
    ]
    await context.bot.send_message(chat_id=chat_id, text="Отлично! Я всё забыл. Можем начать общение заново :)")

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id

    if chat_id not in conversation_histories:
        conversation_histories[chat_id] = [
            {"role": "system", "content": "Ты мой личный друг и собеседник. Общайся со мной тепло, дружелюбно и по-человечески. Отвечай развернуто, но без лишнего официоза, как в живом диалоге."}
        ]

    conversation_histories[chat_id].append({"role": "user", "content": user_text})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_histories[chat_id]
        )
        bot_reply = response.choices[0].message.content
        conversation_histories[chat_id].append({"role": "assistant", "content": bot_reply})
        await context.bot.send_message(chat_id=chat_id, text=bot_reply)

    except Exception as e:
        error_msg = f"Извини, что-то пошло не так. Ошибка: {e}"
        await context.bot.send_message(chat_id=chat_id, text=error_msg)

# === ЗАПУСК БОТА ===
if __name__ == '__main__':
    # Даем время убить старые процессы
    time.sleep(5) 
    
    print("Запускаем бота...")
    
    # Создаем приложение и запускаем его в режиме вебхука, а не поллинга
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('clear', clear_history))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    # Запуск в "веб-режиме" (идеально для Render)
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=f"https://{os.environ.get('RENDER_EXTERNAL_URL', 'localhost')}/webhook"
    )
