from loguru import logger
from bot import run as run_bot


def main():
    logger.add(
        "log/info.log",
        format="{time} {level} {message}", 
        rotation='1 week', 
        level='INFO')
    run_bot()

if __name__ == '__main__':
    main()