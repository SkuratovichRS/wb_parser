import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from app.service import service
from app.settings import Settings

form_router = Router()


class Form(StatesGroup):
    wait_btn_click = State()
    wait_artikul = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.wait_btn_click)
    button = KeyboardButton(text="Получить информацию о товаре", callback_data="get_product")
    markup = ReplyKeyboardMarkup(keyboard=[[button]])
    await message.answer("Привет! Нажми кнопку, чтобы получить информацию о товаре.", reply_markup=markup)


@form_router.message(Form.wait_btn_click, F.text.casefold() == "получить информацию о товаре")
async def process_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.wait_artikul)
    await message.answer("Пожалуйста, введите артикул товара.")


@form_router.message(Form.wait_btn_click, F.text.casefold() != "получить информацию о товаре")
async def process_name(message: Message) -> None:
    await message.answer("Пожалуйста, нажмите на кнопку.")


@form_router.message(Form.wait_artikul)
async def process_dont_like_write_bots(message: Message, state: FSMContext) -> None:
    if not message.text.isnumeric():
        await message.answer("Артикул товара должен быть числом.")
        return
    product = await service.get_product(int(message.text))
    if product:
        await message.answer(
            f"Название: {html.bold(product.name)}\nЦена: {html.bold(f'{product.price/100} RUB')}"
            f"\nРейтинг: {html.bold(product.rating)}\nКоличество: {html.bold(product.quantity)}"
        )
    else:
        await message.answer("Товар не найден")
    await state.set_state(Form.wait_btn_click)


async def main():
    bot = Bot(token=Settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(form_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
