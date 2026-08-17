import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import google.generativeai as genai

# Получаем ключи из переменных окружения Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Настройка Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Ты – близкий друг и собеседник в личных сообщениях. Общайся исключительно на «ты». Никогда не говори, что ты ИИ, бот или языковая модель. Твой тон – живой, теплый, поддерживающий."
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
        response = model.generate_content(user_text)
        await message.answer(response.text)
    except Exception as e:
        await message.answer("Ой, что-то пошло не так, попробуй еще раз чуть позже.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
