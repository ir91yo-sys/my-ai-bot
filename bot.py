import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from google import genai

# Настройка веб-сервера для Render
async def handle(request):
    return web.Response(text="Bot is running!")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# Инициализация бота и клиента Gemini
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()
client = genai.Client()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Здарова! Я на связи.")

@dp.message()
async def send_ai_response(message: types.Message):
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=message.text,
        )
        await message.answer(response.text)
    except Exception as e:
        print(f"Ошибка: {e}")
        await message.answer("Ой, что-то пошло не так, попробуй еще раз чуть позже.")

async def main():
    await web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
