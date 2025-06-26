import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import asyncio
import sys
import logging
from src.bot.bot import init_bot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def run():
    polling_task = None  # инициализируем заранее, чтобы избежать ошибки
    try:
        bot = await init_bot()
        logger.info("Бот успешно инициализирован")

        polling_task = asyncio.create_task(bot.run_polling())

        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        logger.info("Получен сигнал прерывания, останавливаю бота")
    except Exception as e:
        logger.error(f"Ошибка в работе бота: {e}", exc_info=True)
    finally:
        if polling_task:  # Проверяем, была ли задача создана
            polling_task.cancel()
            try:
                await polling_task  # Ожидаем завершения (может вызвать CancelledError)
            except asyncio.CancelledError:
                logger.info("Polling task корректно завершён")
            except Exception as e:
                logger.error(f"Ошибка при завершении polling: {e}")

        logger.info("Бот завершил работу")


def main():
    # для Windows: установка правильной политики цикла событий (Исправляет проблемы с asyncio на Windows, без этого могут возникать ошибки RuntimeError)
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        # обработка остановки пользователем
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.critical(f"Фатальная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()