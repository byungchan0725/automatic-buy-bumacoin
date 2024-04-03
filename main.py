import requests
import json

# 로그인 정보
login_data = {
    "id": "",
    "pw": ""
}

bsm_login_url = "https://auth.bssm.kro.kr/api/auth/login"
coin_price_url = "https://buma.wiki/api/coins/prices"

price = 0
access_token = None
access_refreshToken = None


def login():
    global access_token, access_refreshToken
    try:
        login_response = requests.post(bsm_login_url, json=login_data)

        if login_response.status_code == 200:
            print("로그인이 성공적으로 완료되었습니다.")
            print(login_response)

            # 로그인 성공 시 액세스 토큰 획득
            login_json_response = login_response.json()
            access_token = login_json_response.get("accessToken")
            access_refreshToken = login_json_response.get("refreshToken")

            # 코인 가격 확인
            get_price()

            token()

            buy_coin()

        else:
            print('error')

    except requests.exceptions.RequestException as e:
        print("요청에 실패하였습니다:", e)


def get_price():
    global price
    response = requests.get(coin_price_url)

    if response.status_code == 200:
        json_data = response.json()
        price = json_data["price"]
        print(f"현재 코인 가격: {price}")
    else:
        print('Failed to retrieve the page. Status code:', response.status_code)

    return price


def token():
    global access_token
    url = 'https://auth.bssm.kro.kr/api/oauth/authorize'
    headers = {
        'Cookie': f'bsm_auth_refresh_token_v1={access_refreshToken}; bsm_auth_token_v1={access_token}',
    }

    data = {"clientId": "22fb2e30", "redirectURI": "https://buma.wiki/oauth"}
    response_auth = requests.post(url, headers=headers, json=data)

    text = response_auth.text

    result = text[45:77]

    # 토큰 요청
    url = 'https://buma.wiki/api/auth/oauth/bsm'

    headers = {
        'Cookie': f'bsm_auth_refresh_token_v1={access_refreshToken}; bsm_auth_token_v1={access_token}',
        'Authcode': f'{result}',
    }

    data = {"clientId": "22fb2e30", "redirectURI": "https://buma.wiki/oauth"}

    response_token = requests.post(url, json=data, headers=headers)

    # 서버 응답에서 Authorization 헤더의 내용 가져오기
    data = response_token.text

    # JSON 파싱하여 파이썬 객체로 변환
    parsed_data = json.loads(data)

    access_token = parsed_data["accessToken"]
    print(access_token)


def buy_coin():
    coin_url = 'https://buma.wiki/api/coins/buy'

    headers = {
        "Authorization": f"{access_token}"
    }

    coin_data = {
        'coinPrice': price,
        'coinCount': 1
    }

    coin_response = requests.post(coin_url, json=coin_data, headers=headers)

    if coin_response.status_code == 200:
        print("코인 구매 요청이 성공했습니다.")
        print("응답 데이터:", coin_response.json())
    else:
        print("코인 구매 요청이 실패했습니다. 상태 코드:", coin_response.status_code)


login()
