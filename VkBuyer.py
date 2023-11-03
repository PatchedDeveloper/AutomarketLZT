
import requests
import json
import time
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message

filename = 'login_data'
# Authorization token on the market
headers = {
    "accept": "application/json",
    "authorization": "Bearer 0c8e59d74f79e2ad33d4aa2415fa17bbae6ff54f"
}

# Counter
counter = 0

bot = Bot("6929116139:AAGMUHoYuUFnLtbfYUOXqF1QFKX39aSPWvs")
dp = Dispatcher()

target_chat_id = 930429616

async def send_purchase_message(text):
    await bot.send_message(chat_id=target_chat_id, text=text)

def buy_account(item_id, price, headers):
    url_buy = f"https://api.lzt.market/{item_id}/fast-buy?price={price}"
    response = requests.post(url_buy, headers=headers)

    if response.status_code == 200:
        print(f"Покупка аккаунта {item_id} успешно выполнена за {price} руб.")
        asyncio.create_task(send_purchase_message(f"Покупка аккаунта https://lzt.market/{item_id}/ успешно выполнена за {price} руб."))
    else:
        print(f"Ошибка при покупке аккаунта {item_id}: {response.status_code}")

# CONFIG
price_min = "5"
price_max = "15"

async def main():
    global counter

    while True:
        print(f"\nПопытка № {counter}")

        # Link with parameters
        url = f"https://api.lzt.market/vkontakte?pmin={price_min}&pmax={price_max}&min_age=18&max_age=25&vk_friend_min=100&vk_country[]=Россия&order_by=price_to_up"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()
                items = data.get("items", [])
                total_items = data["totalItems"]

                print(f"\nНайдено {total_items} аккаунтов:")
                print(f"\nНачинаю поиск подходящих вариантов...\n")

                # Purchase account
                for item in items:
                    item_id = item.get("item_id")
                    price = item.get("price")
                    buy_account(item_id, price, headers)

            except json.JSONDecodeError:
                print("JSON ответ не может быть распарсен")
        else:
            print("Ошибка при запросе:", response.status_code)

        counter += 1
        await asyncio.sleep(300)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
