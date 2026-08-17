import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from google import genai
from google.genai import types as genai_types

# 1. Системная инструкция для бота
SYSTEM_INSTRUCTION = """
Ты — живой, интересный собеседник в Telegram. Общайся строго на «ты».
Основные правила общения:
1. Никакой духоты и формализма. Пиши просто, как живой человек в мессенджере, короткими сообщениями.
2. Избегай канцеляризмов, сложных терминов и заумных фраз.
3. Уважай личные границы: если собеседник отвечает холодно или односложно, не будь навязчивым.
"""

# 2. Настройка веб-сервера для Render
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

# 3. Инициализация бота и клиента Gemini
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()
client = genai.Client()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Здарова! Я на связи.")

@dp.message()
async def send_ai_response(message: types.Message):
    try:
        # 4. Запрос к Gemini с системной инструкцией
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=message.text,
            config=genai_types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
            )
        )
        await message.answer(response.text)
    except Exception as e:
        print(f"Ошибка: {e}")
        await message.answer("Ой, что-то пошло не так, попробуй еще раз чуть позже.")

async def main():
    # Запускаем веб-сервер и бота
    await web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
