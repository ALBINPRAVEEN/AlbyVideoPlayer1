#!/usr/bin/env python3

from pyrogram.handlers import InlineQueryHandler
from youtubesearchpython import VideosSearch
from config import Config
from utils import LOGGER
from pyrogram.types import (
    InlineQueryResultArticle, 
    InputTextMessageContent, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)
from pyrogram import (
    Client, 
    errors
)


buttons = [
    [
        InlineKeyboardButton('⚡️DEV', url='https://albinpraveen.ml/portfolio'),
        InlineKeyboardButton('🧩 Report Bug', url='https://t.me/i_am_albin_praveen'),
    ]
    ]
def get_cmd(dur):
    if dur:
        return "/play"
    else:
        return "/stream"
@Client.on_inline_query()
async def search(client, query):
    answers = []
    if query.query == "ETHO_ORUTHAN_PM_VANNU":
        answers.append(
            InlineQueryResultArticle(
                title="Deploy",
                input_message_content=InputTextMessageContent(f"{Config.REPLY_MESSAGE}\n\n<b>You can't use this bot in your group, contact @i_am_albin_praveen.</b>", disable_web_page_preview=True),
                reply_markup=InlineKeyboardMarkup(buttons)
                )
            )
        await query.answer(results=answers, cache_time=0)
        return
    string = query.query.lower().strip().rstrip()
    if string == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text=("Search a youtube video"),
            switch_pm_parameter="help",
            cache_time=0
        )
    else:
        videosSearch = VideosSearch(string.lower(), limit=50)
        for v in videosSearch.result()["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=v["title"],
                    description=("Duration: {} Views: {}").format(
                        v["duration"],
                        v["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "{} https://www.youtube.com/watch?v={}".format(get_cmd(v["duration"]), v["id"])
                    ),
                    thumb_url=v["thumbnails"][0]["url"]
                )
            )
        try:
            await query.answer(
                results=answers,
                cache_time=0
            )
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text=("Nothing found"),
                switch_pm_parameter="",
            )


__handlers__ = [
    [
        InlineQueryHandler(
            search
        )
    ]
]
