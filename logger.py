import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "my_app") -> logging.Logger:
    # Создаем логгер с заданным именем
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Консольный вывод
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # Файловый вывод
    file_handler = RotatingFileHandler(
        'app.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    # Добавляем обработчики к логгеру
    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


# Создаем экземпляр логгера
logger = setup_logger()

