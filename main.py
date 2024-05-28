import requests
import base64
import time
from config import TELEGRAM_TOKEN
from random import randint
from aiogram import Bot, Dispatcher, types, executor
from neiro import get_response
from neir import get_response1
from nei import get_response2
from ne import get_response3

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command='/start', description='Запуск бота'),
        types.BotCommand(command='/joke', description='Шутка'),
        types.BotCommand(command='/cat', description='Факты о котиках'),
        types.BotCommand(command='/coffee', description='Десерты к кофе')
    ]
    await bot.set_my_commands(commands)

@dp.message_handler(commands= 'start')
async def func_start(message: types.Message):
    await message.answer('Привет, я твой шедеврум на максималках')

@dp.message_handler(commands= 'joke')
async def joke(message: types.Message):
    text = message.get_args()
    print(text)
    response_joke = await get_response1(text)
    await message.answer(response_joke)

@dp.message_handler(commands= 'cat')
async def cat(message: types.Message):
    text1 = message.get_args()
    print(text1)
    response_cat = await get_response2(text1)
    await message.answer(response_cat)

@dp.message_handler(commands= 'coffee')
async def coffee(message: types.Message):
    text2 = message.get_args()
    print(text2)
    response_coffee = await get_response3(text2)
    await message.answer(response_coffee)

def generate_image(prompt_text):

    prompt = {
        "modelUri": "art://b1g3f13cj7d6d3ss2md9/yandex-art/latest",
        "generationOptions": {
          "seed": randint(10000, 200000000)
    },
    "messages": [
          {
            "weight": 1,
            "text": prompt_text
          }
    ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key AQVN1ZOzJFEIPSlhC2zZhMGldhqorWGq9YCnYERj"
    }

    response = requests.post(url=url, headers=headers, json=prompt)
    result = response.json()
    print(result)

    operation_id = result['id']

    operation_url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"

    while True:
        operation_response = requests.get(operation_url, headers=headers)
        operation_result = operation_response.json()
        if 'response' in operation_result:
            image_base64 = operation_result['response']['image']
            image_data = base64.b64decode(image_base64)
            return image_data
        else:
            time.sleep(5)

@dp.message_handler()
async def analize_message(message: types.Message):
    response_text = await get_response(message.text)
    print(response_text)
    await message.reply('Идет генерация изображения, подождите пожавуста')
    try:
        image_data = generate_image(response_text)
        await message.reply_photo(photo=image_data)
    except Exception as e:
        await message.reply(f'Произошла ошибка {e}')

async def on_startup(dispatcher):
    await set_commands(dispatcher.bot)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup= on_startup)