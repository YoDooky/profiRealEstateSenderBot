import re
from telegram import aux_funcs, markups
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from excel_module import ExcelData
from database.models.utils import dbcontrol
from database.controllers import messages_controller
from config.bot_config import USERS_FILEPATH, USER_MESSAGES_GROUP_ID
from config.db_config import USERS_FOR_OFFER_TABLE


class DocumentItem(StatesGroup):
    waiting_for_user_choice = State()
    waiting_for_document = State()
    waiting_for_period = State()  # period between sending offers (sec)
    waiting_for_start_time = State()  # start time for sending offers
    waiting_for_sending_messages = State()


class UserMenu:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.offer_loop = aux_funcs.OfferLoop(bot)

    @staticmethod
    def check_auth(decorated_func):
        """Auth decorator"""

        def inner(*args, **kwargs):
            decorated_func(*args, **kwargs)

        return inner

    @staticmethod
    async def wait_for_task_complete(call: types.CallbackQuery, state: FSMContext):
        left_users = aux_funcs.check_current_task(USERS_FOR_OFFER_TABLE)
        keyboard = markups.get_continue_last_offer_menu()
        await call.message.edit_text(
            text=f'⚠ В данный момент бот занят рассылкой офферов {left_users} оставшимся юзерам\n'
                 f'Нажмите "Отмена" если хотите прервать рассылку и начать новую или "Продолжить рассылку", '
                 f'чтобы продолжить предъидущую рассылку',
            reply_markup=keyboard)

    @staticmethod
    async def check_task_exist(call: types.CallbackQuery, state: FSMContext):
        await state.finish()
        left_users = aux_funcs.check_current_task(USERS_FOR_OFFER_TABLE)
        if not left_users:
            keyboard = markups.get_approve_button(callback='choose_file')
            await call.message.edit_text(text='Бот сейчас свободен, нажмите "Подтвердить" 🧐', reply_markup=keyboard)
            return
        keyboard = markups.get_interrupt_current_task_menu()
        await call.message.edit_text(text=f'⚠ В текущем задании на рассылку офферов осталось {left_users} юзеров\n'
                                          f'Вы действительно хотите начать '
                                          f'новую рассылку?',
                                     reply_markup=keyboard)

    @staticmethod
    async def user_choice(call: types.CallbackQuery, state: FSMContext):
        await state.finish()
        # api_user_id = 5871658703
        # second_numb_id = 5936371531
        await call.message.edit_text(text='Отправьте мне excel файл с ID пользователей и оффером 🧐')
        await state.set_state(DocumentItem.waiting_for_document.state)

    async def begin_new_offer(self, message: types.Message, state: FSMContext):
        """Select document with users ID and offer text"""
        if not message.document.file_name.split('.')[-1] == 'xlsx':
            await message.answer(text='❗ Пожалуйста повторите попытку, файл должен быть в формате xlsx')
            return
        await self.bot.download_file_by_id(message.document.file_id, USERS_FILEPATH)
        dbcontrol.clean_table(table=USERS_FOR_OFFER_TABLE)
        messages_controller.db_write_users_offer_data(table=USERS_FOR_OFFER_TABLE)  # write excel data to db
        await message.answer(text='🕐 Введите время между отправками офферов (в секундах)')
        await state.set_state(DocumentItem.waiting_for_period.state)

    @staticmethod
    async def continue_last_offer(call: types.CallbackQuery, state: FSMContext):
        await call.message.answer(text='🕐 Введите время между отправками офферов (в секундах)')
        # await state.set_state(DocumentItem.waiting_for_period.state)
        await state.set_state(DocumentItem.waiting_for_start_time.state)

    # @staticmethod
    # async def set_sending_offers_start_time(message: types.Message, state: FSMContext):
    #     """Selet time between sending message to another user"""
    #     if not re.findall(r'\d+', message.text):
    #         await message.answer(text='Пожалуйста, введите цифровое значение!')
    #         return
    #     await state.update_data(time_between_sending=message.text)
    #     await message.answer(text='Введите время для старта рассылки офферов в формате hh:mm (пример: 9:00)')
    #     await state.set_state(DocumentItem.waiting_for_start_time.state)

    @staticmethod
    async def approve_start_sending_offers(message: types.Message, state: FSMContext):
        """Select start time for messaging"""
        if not re.findall(r'\d+', message.text):
            await message.answer(text='Пожалуйста, введите цифровое значение!')
            return
        await state.update_data(time_between_sending=message.text)
        # selected_time = aux_funcs.check_time_format(message.text)
        # if not selected_time:
        #     await message.answer(text='❗ Введенное время для старта рассылки не соответствует формату hh:mm\n'
        #                               'Пожалуйста повторите попытку')
        #     return
        # await state.update_data(start_sending_time=selected_time)
        # user_data = await state.get_data()
        keyboard = markups.get_start_messaging_menu()
        await message.answer(text=f'🕐 Периодичность рассылки: каждые {message.text} секунд\n'
                                  f'❕ Нажмите "Подтвердить" для начала рассылки или "Отмена" для повторного ввода данных',
                             reply_markup=keyboard)
        await state.set_state(DocumentItem.waiting_for_sending_messages.state)

    async def send_messages_to_users(self, call: types.CallbackQuery, state: FSMContext):
        """Send offer to users by ID"""
        excel_data = ExcelData(file_name='users')
        user_data = await state.get_data()
        sleep_time = user_data.get("time_between_sending")
        user_offer_data = {
            'users_offer_list': messages_controller.db_read_users_offer_data(table=USERS_FOR_OFFER_TABLE),
            'offer_text': excel_data.read_data_from_excel().offer_text,
            'sleep_time': sleep_time
        }
        await self.offer_loop.start(call, user_offer_data)

    async def stop_offer_loop(self, call: types.CallbackQuery):
        """Stops sending offers to users"""
        await self.offer_loop.stop()
        keyboard = markups.get_continue_send_offer_menu()
        await call.message.answer('🛑 Рассылка остановлена', reply_markup=keyboard)

    async def forward_user_message_to_group(self, message: types.Message):
        """Forwards messages from user to group"""
        user_message = message.text if not message.caption else message.caption
        caption_text = f'имя: {message.from_user.first_name}\n' \
                       f'юзернейм: {message.from_user.mention}\n' \
                       f'текст: {user_message}'
        try:
            photo_id = message.photo[-1].file_id
            await self.bot.send_photo(USER_MESSAGES_GROUP_ID, photo_id, caption=caption_text)
            return
        except Exception as ex:
            pass
        try:
            audio_id = message.voice.file_id
            await self.bot.send_voice(USER_MESSAGES_GROUP_ID, audio_id, caption=caption_text)
            return
        except Exception as ex:
            pass
        try:
            document_id = message.document.file_id
            await self.bot.send_document(USER_MESSAGES_GROUP_ID, document_id, caption=caption_text)
            return
        except Exception as ex:
            pass
        await self.bot.send_message(USER_MESSAGES_GROUP_ID, caption_text)

    def register_handlers(self, dp: Dispatcher):
        """Register handlers"""
        dp.register_callback_query_handler(self.check_task_exist, text='start_app', state='*')
        # dp.register_callback_query_handler(self.check_task_exist, text='cancel', state='*')

        dp.register_callback_query_handler(self.wait_for_task_complete, text='cancel_interrupt', state='*')

        dp.register_callback_query_handler(self.user_choice, text='choose_file', state='*')
        # dp.register_callback_query_handler(self.user_choice, text='cancel_start', state='*')
        # dp.register_callback_query_handler(self.user_choice, text='approve_interrupt', state='*')
        # dp.register_callback_query_handler(self.user_choice, text='cancel_offer', state='*')

        dp.register_message_handler(self.begin_new_offer, content_types=['document'],
                                    state=DocumentItem.waiting_for_document)

        dp.register_callback_query_handler(self.continue_last_offer, text='continue_last_offer', state='*')

        # dp.register_message_handler(self.set_sending_offers_start_time, content_types='text',
        #                             state=DocumentItem.waiting_for_period)

        dp.register_message_handler(self.approve_start_sending_offers, content_types='text',
                                    state=DocumentItem.waiting_for_start_time)

        dp.register_callback_query_handler(self.send_messages_to_users, text='approve_start',
                                           state=DocumentItem.waiting_for_sending_messages)
        # dp.register_callback_query_handler(self.send_messages_to_users, text='continue_offer',
        #                                    state=DocumentItem.waiting_for_sending_messages)

        dp.register_message_handler(self.forward_user_message_to_group,
                                    content_types=['document', 'text', 'photo', 'voice'], state='*')
        # dp.register_message_handler(self.send_messages_to_users, content_types='text',
        #                             state=DocumentItem.waiting_for_sending_messages)
        # dp.register_callback_query_handler(self.send_messages_to_users, text='approve',
        #                                    state=DocumentItem.waiting_for_sending_messages)

        # dp.register_callback_query_handler(start_loop, text='start_offer_loop')
        dp.register_callback_query_handler(self.stop_offer_loop, text='stop_offer_loop', state='*')
