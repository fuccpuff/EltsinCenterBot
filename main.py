# main.py
import asyncio
import nest_asyncio
nest_asyncio.apply()
import logging
from telegram.ext import ApplicationBuilder
from config import TOKEN
from handlers import setup_handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    application = ApplicationBuilder().token(TOKEN).build()
    setup_handlers(application)
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())