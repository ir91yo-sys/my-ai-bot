import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import google.generativeai as genai

# Твои ключи (вставь прямо сюда)
TELEGRAM_TOKEN = ""
GEMINI_API_KEY = ""

# Настройка Gemini
genai.configure(api_key=GEMINI_API_KEY)
# Используем быструю и бесплатную модель Flash
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Ты — близкий друг и собеседник в личных сообщениях. Общайся исключительно на «ты». Никогда не говори, что ты ИИ, бот или языковая модель. Твой тон — живой, теплый, поддерживающий."
)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Здарова! Я на связи.")

@dp.message()
async def chat_with_bot(message: types.Message):
    user_text = message.text
    try:
        # Отправляем сообщение нейросети
        response = model.generate_content(user_text)
        await message.answer(response.text)
    except Exception as e:
        await message.answer("Ой, что-то пошло не так, попробуй еще раз чуть позже.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())