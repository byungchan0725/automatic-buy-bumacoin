import requests
import json
import time
from datetime import datetime


def delay():
    time.sleep(0.5)


class AutoCoin:
    def __init__(self):
        # 입력 받는 값
        self.username = input("부마위키 아이디 입력: ")
        self.password = input("부마위키 비밀번호 입력: ")
        self.want_buy_price = input("원하는 매수 가격 아래로: ")
        self.want_sell_price = input("원하는 매도 가격 위로: ")

        self.access_token = None
        self.access_refreshToken = None

        self.price = 0
        self.property = 0  # 현재 재산
        self.have_coins = 0  # 현재 보유 코인 수

        # URL list
        self.urls = {
            "bsm_login": "https://auth.bssm.kro.kr/api/auth/login",  # 부마위키에 접근하기 위한 token 가져옴
            "bsm_auth_token": "https://auth.bssm.kro.kr/api/oauth/authorize",  # bsm token
            "buma_auth_token": "https://buma.wiki/api/auth/oauth/bsm",  # buman token
            "mine": "https://buma.wiki/api/coins/mine",
            "coin_price": "https://buma.wiki/api/coins/prices",  # 부마위키 코인 가격 확인
            "buy_coin": "https://buma.wiki/api/coins/buy",  # 코인 매수
            "sell_coin": "https://buma.wiki/api/coins/sell"  # 코인 매도
        }

    def show_user_info(self):  # 유저가 입력한 정보 확인하는 페이지
        text = f"""
        \n
        ## 입력된 정보는 다음과 같습니다. ## 

        유저 이름: {self.username}
        원하는 매수 가격 이하 값: {self.want_buy_price}
        원하는 매도 가격 이상 값: {self.want_sell_price}

        """
        print(text)

    def main(self):  # 부마위키 로그인 함수
        try:
            login_data = {
                "id": str(self.username),
                "pw": str(self.password)
            }
            login_response = requests.post(str(self.urls["bsm_login"]), json=login_data)

            if login_response.status_code == 200:
                login_json_response = login_response.json()
                self.access_token = login_json_response.get("accessToken")
                self.access_refreshToken = login_json_response.get("refreshToken")

                # self.show_user_info()

                self.get_token()
                self.mine()
                self.get_coin_price()

                if self.price <= int(self.want_buy_price):
                    self.buy()

                if self.price >= int(self.want_sell_price):
                    self.sell()

                time.sleep(180)

            else:
                print("유저 정보를 다시 확인 바랍니다.")
                exit()

        except requests.exceptions.RequestException as e:
            print("서버에 연결할 수 없음.")

    def get_token(self):  # 토큰 가져오는 함수
        headers = {
            'Cookie': f'bsm_auth_refresh_token_v1={self.access_refreshToken}; bsm_auth_token_v1={self.access_token}',
        }

        data = {"clientId": "22fb2e30", "redirectURI": "https://buma.wiki/oauth"}
        response_auth = requests.post(self.urls["bsm_auth_token"], headers=headers, json=data)

        text = response_auth.text
        result = text[45:77]

        # token 요청
        headers = {
            'Cookie': f'bsm_auth_refresh_token_v1={self.access_refreshToken}; bsm_auth_token_v1={self.access_token}',
            'Authcode': f'{result}',
        }

        data = {"clientId": "22fb2e30", "redirectURI": "https://buma.wiki/oauth"}
        response_token = requests.post(self.urls["buma_auth_token"], json=data, headers=headers)

        data = response_token.text
        parsed_data = json.loads(data)

        self.access_token = parsed_data["accessToken"]
        # print(self.access_token) token 확인

    def get_coin_price(self):  # 코인 가격 가져오는 함수
        response = requests.get(self.urls["coin_price"])

        if response.status_code == 200:
            json_data = response.json()
            self.price = json_data["price"]
            print(f"{datetime.now()}  코인 가격: {self.price}")
        else:
            print('Failed to retrieve the page. Status code:', response.status_code)

    def mine(self):
        headers = {
            "Authorization": f"{self.access_token}"
        }

        response = requests.get(self.urls["mine"], headers=headers)

        if response.status_code == 200:
            json_data = response.json()
            self.property = json_data["money"]
            self.have_coins = json_data["coin"]
        else:
            print('Failed to retrieve the page. Status code:', response.status_code)

    def buy(self):  # 매수 함수
        headers = {
            "Authorization": f"{self.access_token}"
        }

        coin_data = {
            'coinPrice': self.price,
            'coinCount': self.property // self.price  # 전재산 // 현재 가격 = 풀매수
        }

        coin_response = requests.post(self.urls["buy_coin"], json=coin_data, headers=headers)

        if coin_response.status_code == 200:
            print(f"- 코인을 {self.property // self.price}주 매수하였습니다.\n")

    def sell(self):  # 매도 함수
        headers = {
            "Authorization": f"{self.access_token}"
        }

        coin_data = {
            'coinCount': self.have_coins,
            'coinPrice': self.price
        }
        # print(self.have_coins, self.price)

        coin_response = requests.post(self.urls["sell_coin"], json=coin_data, headers=headers)

        if coin_response.status_code == 200:
            print(f"- 코인을 {self.have_coins}주 매도하였습니다.\n")


if __name__ == "__main__":
    hello = AutoCoin()
    hello.show_user_info()
    time.sleep(0.5)

    while True:
        hello.main()

