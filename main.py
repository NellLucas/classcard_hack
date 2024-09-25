# main.py
import time
import warnings
import random

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from utility import chd_wh, get_id, word_get, choice_class, choice_set, classcard_api_post
from learning_types import (
    memorization,
    recall,
    spelling,
    test,
    matching_game,
    matching_game_API,
    quiz_battle
)

warnings.filterwarnings("ignore", category=DeprecationWarning)

def main():
    account = get_id()
    
    time_1 = round(random.uniform(0.7, 1.3), 4)
    time_2 = round(random.uniform(1.7, 2.3), 4)

    # 웹드라이버 초기화
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=options)

    try:
        # 로그인
        driver.get("https://www.classcard.net/Login")
        tag_id = driver.find_element(By.ID, "login_id")
        tag_pw = driver.find_element(By.ID, "login_pwd")
        tag_id.clear()
        tag_id.send_keys(account["id"])
        tag_pw.send_keys(account["pw"])
        driver.find_element(By.CSS_SELECTOR,
                            "#loginForm > div.checkbox.primary.text-primary.text-center.m-t-md > a"
                            ).click()

        time.sleep(1)  # 로그인이 늦어지는 경우를 대비

        class_dict = {}
        class_list_element = driver.find_element(
            By.CSS_SELECTOR,
            "body > div.mw-1080 > div:nth-child(6) > div > div > div.left-menu > div.left-item-group.p-t-none.p-r-lg > div.m-t-sm.left-class-list",
        )
        for class_item, i in zip(
            class_list_element.find_elements(By.TAG_NAME, "a"),
            range(len(class_list_element.find_elements(By.TAG_NAME, "a"))),
        ):
            class_temp = {}
            class_temp["class_name"] = class_item.text
            class_temp["class_id"] = class_item.get_attribute("href").split("/")[-1]
            if class_temp["class_id"] == "joinClass":
                break
            class_dict[i] = class_temp

        if len(class_dict) == 0:
            print("클래스가 없습니다.")
            quit()
        elif len(class_dict) == 1:
            choice_class_val = 0
        else:
            choice_class_val = choice_class(class_dict=class_dict)  # 클래스 선택
        class_id = class_dict[choice_class_val].get("class_id")  # 클래스 아이디 가져오기

        driver.get(f"https://www.classcard.net/ClassMain/{class_id}")  # 클래스 페이지로 이동

        time.sleep(1)  # 로딩 대기

        sets_list = []
        sets_div = driver.find_element(
            By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div"
        )
        sets = sets_div.find_elements(By.CLASS_NAME, "set-items")
        sets_dict = {}
        for set_item, i in zip(sets, range(len(sets))):
            set_temp = {}
            set_temp["card_num"] = (  # 카드 개수 가져오기(10 카드)
                set_item.find_element(By.TAG_NAME, "a").find_element(By.TAG_NAME, "span").text
            )
            set_temp["title"] = set_item.find_element(By.TAG_NAME, "a").text.replace(
                set_temp["card_num"], ""
            )  # 카드 개수 제거
            set_temp["set_id"] = set_item.find_element(By.TAG_NAME, "a").get_attribute(
                "data-idx"
            )  # 세트 아이디 가져오기
            sets_dict[i] = set_temp
        choice_set_val = choice_set(sets_dict)  # 세트 선택

        set_site = (
            f"https://www.classcard.net/set/{sets_dict[choice_set_val]['set_id']}/{class_id}"
        )

        driver.get(set_site)  # 세트 페이지로 이동
        time.sleep(1)

        user_id = int(driver.execute_script("return c_u;"))  # 유저 아이디 가져오기

        ch_d = chd_wh()  # 학습유형 선택

        driver.find_element(By.CSS_SELECTOR,
                            "body > div.test > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > a"
                            ).click()
        driver.find_element(By.CSS_SELECTOR,
                            "body > div.test > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > ul > li:nth-child(1)"
                            ).click()

        html = BeautifulSoup(driver.page_source, "html.parser")  # 페이지 소스를 html로 파싱
        cards_ele = html.find("div", class_="flip-body")  # 카드들을 찾음
        num_d = len(cards_ele.find_all("div", class_="flip-card")) + 1  # 카드의 개수를 구함

        time.sleep(0.5)  # 로딩 대기
        
        word_d = word_get(driver, num_d) # 단어 데이터 수집
        da_e, da_k, da_kn, da_kyn, da_ked, da_sd = word_d

        # 학습 유형 선택
        if ch_d == 1:
            print("암기학습 API 요청 변조를 시작합니다.")
            classcard_api_post(
                user_id=user_id,
                set_id=sets_dict[choice_set_val]["set_id"],
                class_id=class_id,
                view_cnt=num_d,
                activity=1,
            )
        elif ch_d == 2:
            print("리콜학습 API 요청 변조를 시작합니다.")
            classcard_api_post(
                user_id=user_id,
                set_id=sets_dict[choice_set_val]["set_id"],
                class_id=class_id,
                view_cnt=num_d,
                activity=2,
            )
        elif ch_d == 3:
            print("스펠학습 API 요청 변조를 시작합니다.")
            classcard_api_post(
                user_id=user_id,
                set_id=sets_dict[choice_set_val]["set_id"],
                class_id=class_id,
                view_cnt=num_d,
                activity=3,
            )
        elif ch_d == 4:
            match_site = (
            f"https://www.classcard.net/Match/{sets_dict[choice_set_val]['set_id']}?c={class_id}"
            )
            driver.get(match_site)
            matching_game_API.run_matching_game_api(driver, match_site)
        elif ch_d == 5:
            test.run_test(driver, num_d, da_e, da_k, da_kn, da_ked, time_1)
        elif ch_d == 6:
            quiz_battle.run_quiz_battle(driver, da_e, da_k, da_sd)
        elif ch_d == 7:
            memorization.run_memorization(driver, num_d)
        elif ch_d == 8:
            recall.run_recall(driver, num_d, da_e, da_kyn, time_2)
        elif ch_d == 9:
            spelling.run_spelling(driver, num_d, da_e, da_k)
        elif ch_d == 10:
            matching_game.run_matching_game(driver, da_e, da_k)
        else:
            print("프로그램을 종료합니다.")

    finally:
        driver.quit() #웹드라이버 종료

if __name__ == "__main__":
    main()
