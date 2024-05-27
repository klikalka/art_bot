import requests
import base64
import time
from random import randint
from aiogram import Bot, Dispatcher, types, executor

API_KEY = '7371388906:AAH8h4i0YlLM4P9Jf2q05QmfKf8cGupk1hc'
bot = Bot(token= API_KEY)
dp = Dispatcher(bot)

@dp.message_handler(commands= 'start')
async def func_start(message: types.Message):
    await message.answer('Привет, я твой шедеврум на максималках')

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
        print(operation_result)
        if 'response' in operation_result:
            image_base64 = operation_result['response']['image']
            image_data = base64.b64decode(image_base64)
            return image_data
        else:
            time.sleep(5)

@dp.message_handler()
async def handle_message(message: types.Message):
    user_text = message.text
    await message.reply('Идет генерация изображения, подождите пожавуста')
    try:
        image_data = generate_image(user_text)
        await message.reply_photo(photo= image_data)
    except Exception as e:
        await message.reply(f'Произошла ошибка {e}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)