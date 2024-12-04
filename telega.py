import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from config import Config, load_config
from handlers import user_handlers
import llama

logger = logging.getLogger(__name__)

CHANNEL_ID = "-1002210841015"

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher()

    dp.include_router(user_handlers.router)

    @dp.message(Command("start"))
    async def send_welcome(message: types.Message):
        kb = [
            [
                types.KeyboardButton(text="Полезные ссылки"),
                types.KeyboardButton(text="Контактная информация"),
                types.KeyboardButton(text="Задать вопрос")
            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )
        await message.reply("Привет!", reply_markup=keyboard)

    @dp.message(lambda message: message.text == "Полезные ссылки")
    async def send_links(message: types.Message):
        links_text = "Вот несколько полезных ссылок:\n" \
                     "- Телеграмм канал: [https://t.me/gulamta_students](https://t.me/gulamta_students)\n" \
                     "- ВК группа: [https://vk.com/gulamta_msk](https://vk.com/gulamta_msk)"
        await message.answer(links_text, parse_mode="Markdown")

    @dp.message(lambda message: message.text == "Контактная информация")
    async def send_contact_info(message: types.Message):
        contact_text = "Почта:\n" \
                       "- Email: gulamta.bso@mail.ru\n"
        await message.answer(contact_text)

    @dp.message(lambda message: message.text == "Задать вопрос")
    async def forward_to_channel(message: types.Message):
        if message.text == "Задать вопрос":
            await message.answer("Задай свой вопрос")
            await bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
