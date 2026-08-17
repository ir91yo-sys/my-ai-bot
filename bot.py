import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from google import genai

# Инициализация бота и клиента Gemini
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()

# Новый клиент корректно подхватывает ключ из переменной окружения GEMINI_API_KEY
client = genai.Client()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Здарова! Я на связи.")

@dp.message()
async def send_ai_response(message: types.Message):
    try:
        # Отправляем запрос к актуальной модели gemini-2.5-flash
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
        )
        await message.answer(response.text)
    except Exception as e:
        print(f"Ошибка: {e}")
        await message.answer("Ой, что-то пошло не так, попробуй еще раз чуть позже.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
