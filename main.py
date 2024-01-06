import logging
import threading
from bot import run as run_bot
from config.config import log_level


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s - %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
    logging.basicConfig(level=log_level)
    run_bot()

if __name__ == '__main__':
    main()