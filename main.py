import requests
import time

from buy_coin import buy_coin_macro


# 이 부분 수정해주세요.
# ***************************************

want_coin_value = 50000  # 원하는 가격 밑으로 적어주셈 (ex 5만원 이하로 떨어졌을때 산다.)
bssm_id = "bsm 아이디"  # bsm id 적어주셈
bssm_password = "bsm 비밀번호"  # bsm password 적어주셈

# ***************************************

def res():
    time.sleep(180)


def get_coin_price():
    url = 'https://buma.wiki/api/coins/prices'

    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        price = json_data["price"]

        if price <= want_coin_value:
            buy_coin_macro(bssm_id, bssm_password)

    else:
        print('Failed to retrieve the page. Status code:', response.status_code)


def main():
    while True:
        get_coin_price()
        res()


if __name__ == "__main__":
    main()
