from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_start_menu() -> InlineKeyboardMarkup:
    start_menu = InlineKeyboardMarkup(row_width=1)
    start_button = InlineKeyboardButton(text='🤖Начать работу с ботом🤖', callback_data='start_app')
    start_menu.insert(start_button)
    return start_menu


# def get_user_menu():
#     user_menu = InlineKeyboardMarkup(row_width=2)
#     get_group_list_button = InlineKeyboardButton(text='Список групп', callback_data='get_group_list')
#     faq_button = InlineKeyboardButton(text='ℹ Справка', callback_data='faq')
#     user_menu.insert(get_group_list_button)
#     user_menu.insert(faq_button)
#     return user_menu


# def get_groups_menu(groups_list):
#     group_menu = InlineKeyboardMarkup(row_width=1)
#     add_group_buttons(groups_list=groups_list, group_menu=group_menu)
#     back_button = InlineKeyboardButton(text='👈 Вернуться назад', callback_data='back')
#     group_menu.insert(back_button)
#     return group_menu


def get_continue_send_offer_menu():
    start_send_offer_menu = InlineKeyboardMarkup(row_width=2)
    start_button = InlineKeyboardButton(text='🤖 Продолжить рассылку', callback_data='approve_start')
    stop_button = InlineKeyboardButton(text='❌ Отмена', callback_data='choose_file')
    start_send_offer_menu.insert(start_button)
    start_send_offer_menu.insert(stop_button)
    return start_send_offer_menu


def get_continue_last_offer_menu():
    start_send_offer_menu = InlineKeyboardMarkup(row_width=2)
    start_button = InlineKeyboardButton(text='🤖 Продолжить рассылку', callback_data='continue_last_offer')
    stop_button = InlineKeyboardButton(text='❌ Отмена', callback_data='choose_file')
    start_send_offer_menu.insert(start_button)
    start_send_offer_menu.insert(stop_button)
    return start_send_offer_menu


# def add_group_buttons(groups_list, group_menu):
#     for group in groups_list:
#         select_group_button = InlineKeyboardButton(text=f'{group.get("username")}',
#                                                    callback_data=f'selected_group_{group.get("username")}')
#         group_menu.insert(select_group_button)
#     return group_menu


# def get_back_button():
#     back_menu = InlineKeyboardMarkup(row_width=1)
#     back_button = InlineKeyboardButton(text='👈 Вернуться назад', callback_data='back')
#     back_menu.insert(back_button)
#     return back_menu


def get_interrupt_current_task_menu():
    interrupt_current_task_menu = InlineKeyboardMarkup(row_width=2)
    get_approve_button(menu=interrupt_current_task_menu, callback='choose_file')
    get_cancel_button(menu=interrupt_current_task_menu, callback='cancel_interrupt')
    return interrupt_current_task_menu


def get_start_messaging_menu():
    start_messaging_menu = InlineKeyboardMarkup(row_width=2)
    get_approve_button(menu=start_messaging_menu, callback='approve_start')
    get_cancel_button(menu=start_messaging_menu, callback='choose_file')
    return start_messaging_menu


def get_cancel_button(menu=None, callback='cancel'):
    cancel_menu = menu
    if not menu:
        cancel_menu = InlineKeyboardMarkup(row_width=1)
    cancel_button = InlineKeyboardButton(text='❌ Отмена', callback_data=callback)
    cancel_menu.insert(cancel_button)
    return cancel_menu


def get_approve_button(menu=None, callback='approve'):
    approve_menu = menu
    if not menu:
        approve_menu = InlineKeyboardMarkup(row_width=1)
    approve_button = InlineKeyboardButton(text='👍 Подтвердить', callback_data=callback)
    approve_menu.insert(approve_button)
    return approve_menu
