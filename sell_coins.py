import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome 드라이버 생성
driver = webdriver.Chrome()

# 특정 URL 열기
url = "https://buma.wiki/coin"  # 여기에 원하는 웹 페이지의 URL을 넣어주세요
driver.get(url)

def delay_time():
    time.sleep(0.2)


def sell_coin_macro(bssm_id, bssm_password):
    try:
        # 부마위키 로그인 버튼 클릭
        login_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/a/span"))
        )
        login_element.click()
        delay_time()

        # 부마위키 로그인 -> BSM 통합 로그인
        bsm_button_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="modal-wrap"]/div[2]/div[2]/form/div[1]/input'))
        )

        bsm_id = bssm_id  # BSM 아이디
        bsm_button_element.send_keys(bsm_id)
        delay_time()

        # 아이디 입력후 다음 버튼 클릭
        next_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="modal-wrap"]/div[2]/div[2]/form/button'))
        )
        next_element.click()
        delay_time()

        # 비밀번호 입력
        bsm_button_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="modal-wrap"]/div[2]/div[2]/form/div[1]/input'))
        )

        password = bssm_password  # BSM 비밀번호
        bsm_button_element.send_keys(password)
        delay_time()

        # 비밀번호 입력 후 다음 버튼 클릭
        next_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="modal-wrap"]/div[2]/div[2]/form/button'))
        )
        next_element.click()
        delay_time()

        # 인증 버튼 클릭
        next_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="modal-wrap"]/div[2]/div/div/button'))
        )
        next_element.click()
        delay_time()

        coin_button_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/ul/a[7]/span'))
        )
        coin_button_element.click()
        delay_time()

        # 매도 버튼 클릭
        sell_button_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/main/div/main/div[2]/div/div/div[2]'))
        )
        sell_button_element.click()
        delay_time()

        # 현재 보유 코인 수
        have_coins = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[3]/div[1]/main/div/main/div[2]/div/figure[2]/span"))
        )

        coins = have_coins.text
        numbers = re.findall(r'\d+', coins)
        numbers_text = ''.join(numbers)
        # print(numbers_text) # 보유 코인 수 출력

        # 값 입력란
        sell_coin_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[3]/div[1]/main/div/main/div[2]/div/figure[3]/input'))
        )

        coins = numbers_text
        sell_coin_element.send_keys(coins)
        delay_time()


        # 최종 매도 버튼 클릭
        confirm_button_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/ html / body / div[3] / div[1] / main / div / main / div[2] / div / button'))
        )
        confirm_button_element.click()
        delay_time()


        # confirm 버튼
        confirm = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/ html / body / div[2] / div / div / div[4] / button[2]'))
        )
        confirm.click()
        delay_time()

    finally:
        print("성공적으로 매도 하였습니다.")
