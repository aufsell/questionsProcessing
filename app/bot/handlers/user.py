from aiogram import Router, F
import sys,os
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, ContentType
sys.path.append(os.path.join(os.getcwd(), 'app'))
print(sys.path)
from bot.db_api import check_user_existence
from bot.keyboards.keyboard import contact_keyboard, approve_register
router = Router()


class Registration_states(StatesGroup):
    name = State()
    last_name = State()
    phone_number = State()
    check_all = State()


# Общая реализация общего меню
async def start_common(msg_or_call, state):
    await state.clear()
    user_id = msg_or_call.from_user.id
    if await check_user_existence(user_id):
        await msg_or_call.answer(
            #TODO доделать мэйн меню
            f'ТЫ УЖЕ ЗАРЕГАН, id {user_id}\n СДЕЛАЮ ПОЗЖЕ МЕЙН ЭКРАН', 
            )
    else:
        await state.set_state(Registration_states.name),
        await msg_or_call.answer(
            f'Привет! Давай зарегистрируемся! Напиши свое имя:', 
            )

# если start ввели командой
async def start(msg: Message, state: FSMContext):
    await start_common(msg, state)


# если start вызвана inline
async def call_start(call: CallbackQuery, state: FSMContext):
    await start_common(call, state)


async def name(msg: Message, state: FSMContext):
    await state.set_state(Registration_states.last_name)
    await state.update_data(name=msg.text)
    await msg.answer('Теперь напиши свою фамилию')

#TODO добавить валидацию
async def last_name(msg: Message, state: FSMContext):
    keyboard = await contact_keyboard()
    await state.set_state(Registration_states.phone_number)
    await state.update_data(last_name=msg.text)
    await msg.answer('Теперь напиши свой номер телефона', reply_markup=keyboard)


async def phone_number(msg: ContentType.CONTACT, state: FSMContext):
    await state.set_state(Registration_states.check_all)

    phone_number = msg.text if isinstance(msg, Message) else msg.contact.phone_number
    await state.update_data(phone_number=phone_number)
    data = await state.get_data()

    await msg.answer(
        f'Проверь все ли введено верно:\n'
        f'Имя: {data["name"]}\n'
        f'Фамилия: {data["last_name"]}\n'
        f'Номер телефона: {data["phone_number"]}\n'
        f'Если все верно, нажми "Зарегистрироваться"',
        reply_markup= await approve_register()
        )

async def check_all_approve(msg: Message, state: FSMContext):
    #TODO вывести меню
    # добавить в бд
    await msg.answer('Зарегистрирован')
    await state.clear()

async def check_all_reject(msg: Message, state: FSMContext):
    await state.set_state(Registration_states.name)
    await msg.answer('Давай заново, напиши свое имя:')


handler_mappings = {
    router.message.register: [
        (start, Command("start")),
        (name, Registration_states.name, F.text),
        (last_name, Registration_states.last_name, F.text),
        (phone_number, Registration_states.phone_number, F.contact | F.text),
        (check_all_approve, Registration_states.check_all, F.text=='Зарегистрироваться'),
        (check_all_reject, Registration_states.check_all, F.text=='Заново'),

    ],
    router.callback_query.register: [
        (call_start, F.data == "start"),

    ]
}

for register_method, handlers in handler_mappings.items():
    for args in handlers:
        register_method(*args)

