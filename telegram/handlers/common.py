from aiogram import types, Dispatcher
from telegram import markups
from aiogram.dispatcher import FSMContext


async def start_command(message: types.Message, state: FSMContext):
    if message.chat.type != 'private':  # start only in private messages
        return
    await state.finish()
    keyboard = markups.get_start_menu()
    await message.answer("👋Добро пожаловать в бот для рассылки сообщений пользователям!\n"
                         "🧐Через меня вы сможете отправить сообщения",
                         reply_markup=keyboard)


def register_handlers(dp: Dispatcher):
    """Register message handlers"""
    dp.register_message_handler(start_command, commands="start", state='*')
