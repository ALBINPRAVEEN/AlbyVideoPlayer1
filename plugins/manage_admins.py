#!/usr/bin/env python3

from utils import LOGGER
from config import Config
from pyrogram import (
    Client, 
    filters
)
from utils import (
    get_admins, 
    sync_to_db, 
    delete_messages,
    sudo_filter
)


@Client.on_message(filters.command(['vcpromote', f"vcpromote@{Config.BOT_USERNAME}"]) & sudo_filter)
async def add_admin(client, message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.id is None:
            k = await message.reply("You are an anonymous admin, you can't do this.")
            await delete_messages([message, k])
            return
        user_id=message.reply_to_message.from_user.id
        user=message.reply_to_message.from_user

    elif ' ' in message.text:
        c, user = message.text.split(" ", 1)
        if user.startswith("@"):
            user=user.replace("@", "")
            try:
                user=await client.get_users(user)
            except Exception as e:
                k=await message.reply(f"I was unable to locate that user.\nError: {e}")
                LOGGER.error(f"Unable to find the user - {e}", exc_info=True)
                await delete_messages([message, k])
                return
            user_id=user.id
        else:
            try:
                user_id=int(user)
                user=await client.get_users(user_id)
            except:
                k=await message.reply(f"You should give a user id or his username with @.")
                await delete_messages([message, k])
                return
    else:
        k=await message.reply("No user specified, reply to a user with /vcpromote or pass a users user id or username.")
        await delete_messages([message, k])
        return
    if user_id in Config.ADMINS:
        k = await message.reply("This user is already an admin.") 
        await delete_messages([message, k])
        return
    Config.ADMINS.append(user_id)
    k=await message.reply(f"Succesfully promoted {user.mention} as VC admin")
    await sync_to_db()
    await delete_messages([message, k])


@Client.on_message(filters.command(['vcdemote', f"vcdemote@{Config.BOT_USERNAME}"]) & sudo_filter)
async def remove_admin(client, message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.id is None:
            k = await message.reply("You are an anonymous admin, you can't do this.")
            await delete_messages([message, k])
            return
        user_id=message.reply_to_message.from_user.id
        user=message.reply_to_message.from_user
    elif ' ' in message.text:
        c, user = message.text.split(" ", 1)
        if user.startswith("@"):
            user=user.replace("@", "")
            try:
                user=await client.get_users(user)
            except Exception as e:
                k = await message.reply(f"I was unable to locate that user.\nError: {e}")
                LOGGER.error(f"Unable to Locate user, {e}", exc_info=True)
                await delete_messages([message, k])
                return
            user_id=user.id
        else:
            try:
                user_id=int(user)
                user=await client.get_users(user_id)
            except:
                k = await message.reply(f"You should give a user id or his username with @.")
                await delete_messages([message, k])
                return
    else:
        k = await message.reply("No user specified, reply to a user with /vcdemote or pass a users user id or username.")
        await delete_messages([message, k])
        return
    if not user_id in Config.ADMINS:
        k = await message.reply("This user is not an admin yet.")
        await delete_messages([message, k])
        return
    Config.ADMINS.remove(user_id)
    k = await message.reply(f"Succesfully Demoted {user.mention}")
    await sync_to_db()
    await delete_messages([message, k])


@Client.on_message(filters.command(['refresh', f"refresh@{Config.BOT_USERNAME}"]) & filters.user(Config.SUDO))
async def refresh_admins(client, message):
    Config.ADMIN_CACHE=False
    await get_admins(Config.CHAT)
    k = await message.reply("Admin list has been refreshed")
    await sync_to_db()
    await delete_messages([message, k])
