import os, asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession

# Ссылка на вашу игру на GitHub Pages
APP_URL = "https://andreirakit2009-oss.github.io/life-game/index.html?v=2" 

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Если бот не подключается без VPN, раскомментируйте строку ниже и впишите ваш порт (убрать #)
# PROXY_URL = "socks5://127.0.0.1:10808"
PROXY_URL = None

if PROXY_URL:
    session = AiohttpSession(proxy=PROXY_URL)
    bot = Bot(BOT_TOKEN, session=session)
    print("Запуск через прокси...")
else:
    bot = Bot(BOT_TOKEN)
    print("Запуск без прокси...")

dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def start(m: Message):
    # Создаем кнопку, которая открывает Web App (мини-приложение)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Играть", web_app=WebAppInfo(url=APP_URL))]
    ])
    await m.answer("Добро пожаловать в «1 из 8 миллиардов»!\nНажми кнопку ниже, чтобы начать.", reply_markup=kb)

async def main():
    print("Бот запущен! Ожидание команды /start...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())