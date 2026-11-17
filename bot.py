import os, asyncio, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession

# Ссылка на вашу игру на GitHub Pages
APP_URL = "https://andreirakit2009-oss.github.io/life-game/index.html"

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Если бот не подключается без VPN, раскомментируйте строку ниже
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
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Играть", web_app=WebAppInfo(url=APP_URL))]
    ])
    await m.answer("Добро пожаловать в «1 из 8 миллиардов»!\nНажми кнопку ниже, чтобы начать.", reply_markup=kb)

# --- МИНИ-ВЕБ-СЕРВЕР ДЛЯ RENDER ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    print(f"Веб-сервер запущен на порту {port}")
    server.serve_forever()

async def main():
    # Запускаем веб-сервер в отдельном потоке, чтобы он не блокировал бота
    threading.Thread(target=run_health_check, daemon=True).start()
    
    print("Бот запускается... Ожидание команды /start...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
