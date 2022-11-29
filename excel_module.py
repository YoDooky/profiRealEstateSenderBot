import sys
from typing import Dict, List
from app_types import Offers
import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import json


class ExcelData:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.full_file_path = f'C:/PyProject/profiRealEstateSenderBot/excel/{file_name}.xlsx'

    def __create_excel_file(self):
        """Creating file with data"""
        wb = openpyxl.Workbook()
        wb.save(self.full_file_path)
        workbook = load_workbook(filename=self.full_file_path)
        workbook.worksheets[0].title = 'data'
        wb.save(self.full_file_path)
        return workbook

    def __get_json_data(self):
        """Get data from json"""
        try:
            with open(f'json/{self.file_name}.json', 'r', encoding='utf-8') as file:
                return json.loads(file.read())
        except Exception as ex:
            print(f'[FATAL] Cant open json file with data. Script shutdown,\n{ex}')
            sys.exit()

    @staticmethod
    def translate_header(raw_headers: Dict) -> List[str]:
        translated_headers = []
        for key, value in raw_headers.items():
            if key == 'first_name':
                translated_headers.append('имя')
            if key == 'last_name':
                translated_headers.append('фамилия')
            if key == 'username':
                translated_headers.append('юзернейм')
            if key == 'phone':
                translated_headers.append('номер телефона')
            if key == 'phone_calls_available':
                translated_headers.append('доступен для звонка')
            if key == 'id':
                translated_headers.append('ID пользователя')
            if key == 'was_online':
                translated_headers.append('был онлайн')
        return translated_headers

    def write_data_to_excel(self):
        """Write data to excel"""
        workbook = self.__create_excel_file()
        src_file = self.__get_json_data()

        sheet = 'data'
        excel_column = 1
        excel_row = 1
        # write headers
        color_code = '9FC5E8'
        headers_list = self.translate_header(src_file[0])
        for header in headers_list:
            workbook[sheet].cell(row=excel_row, column=excel_column).value = header
            workbook[sheet].cell(row=excel_row, column=excel_column).fill = PatternFill(fgColor=color_code,
                                                                                        fill_type='solid')
            excel_column += 1
        # increase column width
        columns_letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        for column in columns_letter:
            workbook[sheet].column_dimensions[column].width = 20
        # write values
        excel_row = 2
        for data in src_file:
            for num, each in enumerate(data):
                workbook[sheet].cell(row=excel_row, column=num + 1).value = data[each]
                if num >= 6:  # max users columns
                    break
            excel_row += 1

        workbook.save(self.full_file_path)
        workbook.close()

    def read_data_from_excel(self) -> Offers:
        workbook = load_workbook(filename=self.full_file_path)
        users_column = 1
        user_row = 2
        # get all users id
        users_info_list = []
        while workbook.worksheets[0].cell(row=user_row, column=users_column).value:
            users_info_list.append({
                'tg_id': workbook.worksheets[0].cell(row=user_row, column=users_column).value,
                'message_to_user_sends': False
            })
            user_row += 1
        # get offer text
        message_column = 2
        message_row = 2
        offer_text = workbook.worksheets[0].cell(row=message_row, column=message_column).value

        return Offers(users_info=users_info_list, offer_text=offer_text)
