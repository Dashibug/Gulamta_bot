from aiogram import F, Router
from aiogram.types import Message
import openai

from config import load_config

# Устанавливаем ключ API для OpenAI
openai.api_key = load_config().openai_token

# Создаем объект маршрутизатора
router: Router = Router()

# Функция для общения с OpenAI GPT-3
async def chat(text: str) -> str:
    try:
        # Асинхронный запрос к API OpenAI для генерации ответа
        response = await openai.Completion.acreate(
            model="gpt-3.5-turbo",  # Используем подходящую модель
            messages=[{"role": "user", "content": text}],  # Передаем текст как сообщение от пользователя
            temperature=0.5,  # Контролируем степень случайности в ответах
            max_tokens=500  # Ограничиваем количество токенов
        )
        # Возвращаем только текст ответа
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Произошла ошибка при обращении к OpenAI: {e}"

# Обработчик входящих текстовых сообщений
@router.message(F.content_type == 'text')
async def process_message(message: Message):
    """Обрабатывает все текстовые сообщения."""
    # Получаем ответ от OpenAI
    answer = await chat(message.text)
    # Отправляем ответ пользователю
    await message.reply(text=answer)