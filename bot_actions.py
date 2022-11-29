from telegram.telethone import collect_users_data
from telegram.telethone import collect_bot_groups
from telegram.telethone import send_message
from excel_module import ExcelData
from config.bot_config import API_ID, API_HASH, PHONE


async def collect_user_data_from_telegram(group_name: str):
    """Collect data about users from telegram group"""
    api_id = API_ID
    api_hash = API_HASH
    phone = PHONE
    await collect_users_data.bot_init(api_id=api_id, api_hash=api_hash, phone=phone, group_name=group_name)


async def collect_bot_groups_from_telegram():
    """Collect data about bot groups from telegram"""
    api_id = API_ID
    api_hash = API_HASH
    phone = PHONE
    await collect_bot_groups.bot_init(api_id=api_id, api_hash=api_hash, phone=phone)


def write_data_to_excel(group_name: str):
    """Write data collected from telegram"""
    excel_data = ExcelData(group_name)
    excel_data.write_data_to_excel()


async def get_data_from_group(group_name: str):
    """Collect data from telegram groups, write it to excel"""
    await collect_user_data_from_telegram(group_name=group_name)
    write_data_to_excel(group_name=group_name)


async def send_message_to_user():
    """Collect data about bot groups from telegram"""
    api_id = API_ID
    api_hash = API_HASH
    phone = PHONE
    api_user_id = 5871658703
    second_numb_id = 5936371531
    await send_message.bot_init(api_id=api_id, api_hash=api_hash, phone=phone, user_id=5871658703)
