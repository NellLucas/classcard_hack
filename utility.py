import json
import re
from selenium.webdriver.common.by import By
import requests


def word_get(driver, num_d):
    da_e = [0 for _ in range(num_d)]
    da_k = [0 for _ in range(num_d)]
    da_kyn = [0 for _ in range(num_d)]
    da_sd = [0 for _ in range(num_d)]

    for i in range(1, num_d):
        da_e[i] = driver.find_element(By.XPATH,
            f"//*[@id='tab_set_all']/div[2]/div[{i}]/div[4]/div[1]/div[1]/div/div"
        ).text
    for i in range(1, num_d):
        url = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[4]/div[3]/div[1]/div[2]/div[{i}]/div[4]/div[1]/div[3]/a")
        vl = url.get_attribute('data-src')
        lv = vl.split("/")
        lv = list(filter(None, lv))
        for k in range(0, len(lv)):
            if "uploads" in lv[k]:
                for j in range(0, k):
                    del lv[0]
                break
        lv.insert(0, '')
        lv = "/".join(lv)
        da_sd[i] = lv

    driver.find_element(By.CSS_SELECTOR,
        "#tab_set_all > div.card-list-title > div > div:nth-child(1) > a"
    ).click()

    for i in range(1, num_d):
        ko_d = driver.find_element(By.XPATH,
            f"//*[@id='tab_set_all']/div[2]/div[{i}]/div[4]/div[2]/div[1]/div/div"
        ).text
        ko_d = ko_d.split("\n")

        try:
            if bool(re.search(r"[a-z]", ko_d[1])):
                da_k[i] = f"{ko_d[0]}"
                da_kyn[i] = f"{ko_d[0]}"
            else:
                da_k[i] = f"{ko_d[0]}\n{ko_d[1]}"
                da_kyn[i] = f"{ko_d[0]} {ko_d[1]}"
        except:
            da_k[i] = f"{ko_d[0]}"
            da_kyn[i] = f"{ko_d[0]}"

    return [da_e, da_k, da_kyn, da_sd]


def chd_wh():
    print(
        """
Please select a learning type.
[1] 암기학습
[2] 리콜학습
[3] 스펠학습
[4] 테스트학습
[5] 매칭GAME
[6] QuizBattle(Classcard Battle)
    """
    )
    while 1:
        try:
            ch_d = int(input(">>> "))
            if ch_d >= 1 and ch_d <= 6:
                break
            else:
                raise ValueError
        except ValueError:
            print("Please enter the learning type again.")
        except KeyboardInterrupt:
            quit()
    return ch_d


def check_id(id, pw):
    print("계정 정보를 확인하고 있습니다 잠시만 기다려주세요!")
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    data = {"login_id": id, "login_pwd": pw}
    res = requests.post(
        "https://www.classcard.net/LoginProc", headers=headers, data=data
    )
    status = res.json()
    if status["result"] == "ok":
        return True
    else:
        return False


def save_id():
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
            json_data["id"]
            json_data["pw"]
            return json_data
    except:
        return save_id()
