#!/usr/bin/env python3

from logging.handlers import RotatingFileHandler
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            "botlog.txt",
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logging.getLogger("apscheduler").setLevel(logging.ERROR)

LOGGER=logging.getLogger(__name__)


