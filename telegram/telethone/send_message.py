import asyncio
from typing import Dict, List
from telethon.tl.types import InputPeerUser
from telethon import TelegramClient
from database.controllers import messages_controller

from config.db_config import USERS_FOR_OFFER_TABLE
from config.bot_config import API_ID, API_HASH


# async def bot_init(api_id: int, api_hash: str):  # , group_name: str, offer_text: str):
#     """Bot initialization"""
#     client = TelegramClient('84879148411', api_id, api_hash)
#     async with client:
#         # await send_message_by_id(client, group_name, offer_text)
#         await get_group_names(client)


def get_users_for_offer(table: str) -> List[int]:
    """Gets user from db whos dont get an offer"""
    users_id = messages_controller.db_read_users_offer_data(table)
    demand_users_id = []
    for each_id in users_id:
        if each_id.get('message_to_user_sends'):
            continue
        demand_users_id.append(each_id.get('tg_id'))
    return demand_users_id


class GroupData:
    def __init__(self, api_id: int, api_hash: str):
        self.client = TelegramClient('84879148411', api_id, api_hash)

    async def get_group_names(self) -> List[Dict]:
        """Get account groups"""
        async with self.client:
            bot_chats = self.client.iter_dialogs()
            bot_groups = []
            async for chat in bot_chats:
                if not chat.is_group:
                    continue
                try:
                    chat_id = chat.id
                except AttributeError:
                    chat_id = None
                try:
                    username = chat.message.chat.username
                except AttributeError:
                    continue
                try:
                    name = chat.name
                except AttributeError:
                    name = None
                bot_groups.append({
                    'id': chat_id,
                    'username': username,
                    'name': name
                })
            return bot_groups

    async def get_group_members(self, group_name: str) -> List[Dict]:
        """Get members hash and id from group"""
        async with self.client:
            demand_users_id = get_users_for_offer(table=USERS_FOR_OFFER_TABLE)
            user_list = self.client.iter_participants(group_name)
            users_data = []
            async for user in user_list:
                if user.id not in demand_users_id:
                    continue
                users_data.append({
                    'user_id': user.id,
                    'user_hash': user.access_hash
                })
            return users_data

    async def send_message_by_id(self, offer_text: str, user_data: Dict):
        """Send message to user by id"""
        with self.client:
            receiver = InputPeerUser(user_id=user_data.get('user_id'), access_hash=user_data.get('user_hash'))
            await self.client.send_message(receiver, offer_text)


async def main():
    # await bot_init(api_id=API_ID, api_hash=API_HASH)
    group_data = GroupData(api_id=API_ID, api_hash=API_HASH)
    data = await group_data.get_group_names()
    group_members_data = await group_data.get_group_members(data[0].get('username'))
    print(group_members_data)

asyncio.run(main())
