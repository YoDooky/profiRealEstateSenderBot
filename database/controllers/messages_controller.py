from typing import List, Dict
from database.models.utils import dbcontrol
from app_types import Offers
from excel_module import ExcelData


def db_write_users_offer_data(table: str):
    """Write offer data to DB"""
    excel_data = ExcelData(file_name='users')
    data = excel_data.read_data_from_excel()
    for each in data.users_info:
        dbcontrol.insert_db(table, each)


def db_check_send_message(table: str, tg_id: int):
    """Check in db that user get message from bot"""
    row_val = {'tg_id': tg_id}
    column_val = {'message_to_user_sends': True}
    dbcontrol.update_db(table, row_val, column_val)


def db_read_users_offer_data(table: str) -> List[Dict]:
    """Read offer data from db"""
    data_columns = ['tg_id', 'message_to_user_sends']
    return dbcontrol.fetchall(table, data_columns)
