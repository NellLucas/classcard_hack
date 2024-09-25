# utility.py
import time
import json
import re
import os
from selenium.webdriver.common.by import By
import requests

def word_get(driver, num_d) -> list:
    da_e, da_k, da_kn, da_kyn, da_ked, da_sd = [[0] * num_d for _ in range(6)]

    for i in range(1, num_d):
        da_e[i] = driver.find_element(By.XPATH,
            f"//*[@id='tab_set_all']/div[2]/div[{i}]/div[4]/div[1]/div[1]/div/div"
        ).text
    for i in range(1, num_d):
        url = driver.find_element(By.XPATH, f"//*[@id='tab_set_all']/div[2]/div[{i}]/div[4]/div[1]/div[3]/a").get_attribute('data-src')
        lv = [part for part in url.split("/") if part]
        upload_index = next((index for index, part in enumerate(lv) if "uploads" in part), None)
        if upload_index is not None:
            lv = lv[upload_index:]
        da_sd[i] = "/" + "/".join(lv)

    driver.find_element(By.CSS_SELECTOR,
        "#tab_set_all > div.card-list-title > div > div:nth-child(1) > a"
    ).click()
    time.sleep(0.5)
    
    for i in range(1, num_d):
        ko_d = driver.find_element(By.XPATH,
            f"//*[@id='tab_set_all']/div[2]/div[{i}]/div[4]/div[2]/div[1]/div/div"
        ).text
        ko_d = ko_d.split("\n")
        
        #명. 동. 형. 부. 와 같은 품사 표기 제거(options)
        POS_MARKERS = ['명', '동', '형', '부'] 
        pattern = r'\b(?:' + '|'.join(POS_MARKERS) + r')\.\s*'
        edit_ko_d = [re.sub(pattern, '', line) for line in ko_d]

        if len(ko_d) == 1:
            da_k[i] = ko_d[0]
            da_kn[i] = ko_d[0]
            da_kyn[i] = ko_d[0]
            da_ked[i] = edit_ko_d[0]
        else:
            da_k[i] = "\n".join(ko_d)
            da_kn[i] = ", ".join(ko_d)
            da_kyn[i] = " ".join(ko_d)
            da_ked[i] = ", ".join(edit_ko_d)

    return [da_e, da_k, da_kn, da_kyn, da_ked, da_sd]

def chd_wh() -> int:
    print(
        """
학습 유형을 선택해주세요!!
[1] 암기학습(API 요청 변조)
[2] 리콜학습(API 요청 변조)
[3] 스펠학습(API 요청 변조)
[4] 매칭게임(API 요청 변조)
[5] 테스트학습(매크로)
[6] QuizBattle(매크로)
[7] 암기학습(매크로)
[8] 리콜학습(매크로)
[9] 스펠학습(매크로)
[10] 매칭게임(매크로)
---------------------------
Developed by NellLucas(서재형)
    """
    )
    while True:
        try:
            ch_d = int(input(">>> "))
            if 1 <= ch_d <= 10:
                break
            else:
                raise ValueError
        except ValueError:
            print("올바른 학습 유형(1~10)을 선택해주세요.")
        except KeyboardInterrupt:
            print("\n사용자에 의해 종료되었습니다.")
            quit()
    return ch_d

def check_id(id, pw) -> bool:
    print("계정 정보를 확인하고 있습니다... 잠시만 기다리세요!!")
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    data = {"login_id": id, "login_pwd": pw}
    res = requests.post(
        "https://www.classcard.net/LoginProc", headers=headers, data=data
    )
    try:
        status = res.json()
        return status.get("result") == "ok"
    except ValueError:
        return False

def choice_set(sets: dict) -> int:
    os.system("cls")
    print("학습할 세트를 선택해주세요.")
    print("Ctrl + C 를 눌러 종료")
    for set_item in sets:
        print(
            f"[{set_item+1}] {sets[set_item].get('title')} | {sets[set_item].get('card_num')}"
        )
    while True:
        try:
            ch_s = int(input(">>> "))
            if ch_s >= 1 and ch_s <= len(sets):
                break
            else:
                raise ValueError
        except ValueError:
            print("세트를 다시 입력해주세요.")
        except KeyboardInterrupt:
            quit()
    os.system("cls")
    print(f"{sets[ch_s-1].get('title')}를 선택하셨습니다.")
    return ch_s - 1

def choice_class(class_dict: dict) -> int:
    os.system("cls")
    print("학습할 클래스를 선택해주세요.")
    print("Ctrl + C 를 눌러 종료")
    for class_item in class_dict:
        print(f"[{class_item+1}] {class_dict[class_item].get('class_name')}")
    while True:
        try:
            ch_c = int(input(">>> "))
            if ch_c >= 1 and ch_c <= len(class_dict):
                break
            else:
                raise ValueError
        except ValueError:
            print("클래스를 다시 입력해주세요.")
        except KeyboardInterrupt:
            quit()
    os.system("cls")
    print(f"{class_dict[ch_c-1].get('class_name')}를 선택하셨습니다.")
    return ch_c - 1

def save_id() -> dict:
    while True:
        id = input("아이디를 입력하세요 : ")
        password = input("비밀번호를 입력하세요 : ")
        if check_id(id, password):
            data = {"id": id, "pw": password}
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("아이디 비밀번호가 저장되었습니다.\n")
            return data
        else:
            print("아이디 또는 비밀번호가 잘못되었습니다.\n")
            continue

def get_id():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)
            return json_data
    except (FileNotFoundError, json.JSONDecodeError):
        return save_id()

def classcard_api_post(
    user_id: int,
    set_id: int,
    class_id: int,
    view_cnt: int,
    activity: int,
) -> None:
    url = "https://www.classcard.net/ViewSetAsync/resetAllLog"
    payload = f"set_idx={set_id}&activity={activity}&user_idx={user_id}&view_cnt={view_cnt}&class_idx={class_id}"
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    requests.request("POST", url, data=payload, headers=headers)
    print("API 요청 변조에 성공하였습니다!")
