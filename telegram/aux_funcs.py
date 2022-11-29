import re
import asyncio
from typing import Dict
from telegram import markups
from aiogram import Bot
from aiogram import types

from database.controllers import messages_controller
from config.db_config import USERS_FOR_OFFER_TABLE


class OfferLoop:
    def __init__(self, bot: Bot):
        self._active = False
        self._stopped = True
        self.bot = bot

    @property
    def is_running(self):
        return not self._stopped

    async def start(self, call: types.CallbackQuery, user_offer_data: Dict):
        self._active = True
        # иницализировать телетон
        asyncio.create_task(self._run_loop(call, user_offer_data))

    async def _run_loop(self, call: types.CallbackQuery, user_offer_data: Dict):
        """Sending offers and write result to db"""
        for user in user_offer_data.get('users_offer_list'):
            if not self._active:
                break
            if user.get('message_to_user_sends'):
                continue
            # await self.bot.send_message(user.get('tg_id'), user_offer_data.get('offer_text'))
            messages_controller.db_check_send_message(table=USERS_FOR_OFFER_TABLE, tg_id=user.get('tg_id'))
            keyboard = markups.get_cancel_button(callback='stop_offer_loop')
            message_text = f'Сообщение для ID: {user.get("tg_id")} отправлено.\n' \
                           f'Жду {user_offer_data.get("sleep_time")} секунд, перед отправкой ' \
                           f'сообщения для следующего ID...\n' \
                           f'Осталось юзеров для отправки: ' \
                           f'{check_current_task("offers")}'
            if not check_current_task("offers"):
                keyboard = markups.get_approve_button(callback='choose_file')
                message_text = 'Рассылка офферов завершена, нажмите "Подтвердить"'
            await call.message.edit_text(text=message_text, reply_markup=keyboard)
            await asyncio.sleep(int(user_offer_data.get('sleep_time')))
        self._stopped = True

    async def stop(self):
        self._active = False
        while not self._stopped:
            await asyncio.sleep(1)


def send_message_via_telethone():



def check_current_task(table: str) -> int:
    """Get amount of users, who dont get offer in current task"""
    data = messages_controller.db_read_users_offer_data(table)
    left_users = 0
    for each in data:
        if not each.get('message_to_user_sends'):
            left_users += 1
    return left_users


def check_time_format(time_string: str):
    """Return None if time_string is not in format hh:mm"""
    selected_time_list = time_string.split(':')
    try:
        selected_time_list[1]
    except Exception as ex:
        ex
        return None
    if not re.findall(r'\d+', selected_time_list[0]):
        return None
    if int(selected_time_list[0]) > 23 or int(selected_time_list[0]) < 0:
        return None
    if not re.findall(r'\d+', selected_time_list[1]):
        return None
    if int(selected_time_list[1]) > 60 or int(selected_time_list[1]) < 0:
        return None
    return f'{selected_time_list[0]}:{selected_time_list[1]}'
