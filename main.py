import requests
import time

from datetime import datetime

from buy_coin import buy_coin_macro
from sell_coins import sell_coin_macro


want_coin_value_for_buy = 1000000  # 원하는 가격 밑으로 적어주셈 (ex 5만원 이하로 떨어졌을때 산다.)
want_coin_value_for_sell = 2000000 # 원하는 가격 위로 (ex 200만원 위로 올라가면 팔꺼임)
bssm_id = "" #bsm id 적어주셈
bssm_password = ""  # bsm password 적어주셈

price = 0

def res():
    time.sleep(180)


def get_coin_price():
    url = 'https://buma.wiki/api/coins/prices'

    response = requests.get(url)

    if response.status_code == 200:
        global price
        json_data = response.json()
        price = json_data["price"]
        now = datetime.now()
        print(f"현재 시간: {now}, 현재 코인 가격: {price}")
    else:
        print('Failed to retrieve the page. Status code:', response.status_code)


def main():
    while True:
        get_coin_price()

        if price <= want_coin_value_for_buy:
            sell_coin_macro(bssm_id, bssm_password)

        elif price >= want_coin_value_for_sell:
            sell_coin_macro(bssm_id, bssm_password)

        else:
            pass

        res()


if __name__ == "__main__":
    main()
