import time
import warnings
import random

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException, NoSuchElementException)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utility import chd_wh, get_id, word_get

warnings.filterwarnings("ignore", category=DeprecationWarning)
account = get_id()
class_site = input("학습할 세트URL을 입력하세요 : ")
ch_d = chd_wh()
time_1 = round(random.uniform(0.7, 1.3), 4)
time_2 = round(random.uniform(1.7, 2.3), 4)
time_1_5 = round(random.uniform(1.2, 1.8), 4)


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options)


driver.get("https://www.classcard.net/Login")
tag_id = driver.find_element(By.ID, "login_id")
tag_pw = driver.find_element(By.ID, "login_pwd")
tag_id.clear()
tag_id.send_keys(account["id"])
tag_pw.send_keys(account["pw"])
driver.find_element(By.CSS_SELECTOR,
                    "#loginForm > div.checkbox.primary.text-primary.text-center.m-t-md > button"
                    ).click()

try:
    time.sleep(1)
    driver.get(class_site)
    driver.find_elements(By.XPATH, "//div[@class='p-b-sm']")
except:
    print("\n입력한 URL이 잘못되어 프로그램을 종료합니다\n")
    input("종료하려면 아무 키나 누르세요...")
    quit()
time.sleep(1)

driver.find_element(By.CSS_SELECTOR,
                    "body > div.test > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > a"
                    ).click()
driver.find_element(By.CSS_SELECTOR,
                    "body > div.test > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > ul > li:nth-child(1)"
                    ).click()

html = BeautifulSoup(driver.page_source, "html.parser")
cards_ele = html.find("div", class_="flip-body")
num_d = len(cards_ele.find_all("div", class_="flip-card")) + 1

time.sleep(0.5)

word_d = word_get(driver, num_d)

da_e = word_d[0]
da_k = word_d[1]
da_kn = word_d[2]
da_kyn = word_d[3]
da_sd = word_d[4]


while True:
    if ch_d == 1:
        driver.find_element(By.XPATH,
                            "/html/body/div[2]/div/div[2]/div[1]/div[1]"
                            ).click()
        driver.find_element(By.CSS_SELECTOR,
                            "#wrapper-learn > div.start-opt-body > div > div > div > div.m-t > a"
                            ).click()
        for i in range(1, num_d):
            time.sleep(2.5)
            try:
                driver.find_element(By.CSS_SELECTOR,
                                    "#wrapper-learn > div > div > div.study-bottom > div.btn-text.btn-down-cover-box"
                                    ).click()
                time.sleep(0.5)
                driver.find_element(By.CSS_SELECTOR,
                                    "#wrapper-learn > div > div > div.study-bottom.down > div.btn-text.btn-know-box"
                                    ).click()
            except:
                break
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,
                            "body > div.study-header-body > div > div:nth-child(1) > div:nth-child(1) > a"
                            ).click()
    elif ch_d == 2:
        driver.find_element(By.XPATH,
                            "/html/body/div[2]/div/div[2]/div[1]/div[2]"
                            ).click()
        driver.find_element(By.CSS_SELECTOR,
                            "#wrapper-learn > div.start-opt-body > div > div > div > div.m-t > a"
                            ).click()
        time.sleep(time_2)
        for i in range(1, num_d):
            try:
                cash_d = driver.find_element(By.XPATH,
                                             f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i}]/div[1]/div/div/div/div[1]/span"
                                             ).text

                cash_dby = [0, 0, 0]

                for j in range(0, 3):
                    cash_dby[j] = driver.find_element(By.XPATH,
                                                      f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i}]/div[3]/div[{j + 1}]/div[2]/div"
                                                      ).text

                ck = False
                if cash_d.upper() != cash_d.lower():
                    try:
                        for j in range(0, 3):
                            if da_e.index(cash_d) == da_kyn.index(cash_dby[j]):
                                driver.find_element(By.XPATH,
                                                    f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i}]/div[3]/div[{j + 1}]/div[2]"
                                                    ).click()
                                ck = True
                                break
                    except:
                        pass
                    if ck != True:
                        print("\nDetected Missing Words!!, Randomly Selected\n")
                        driver.find_element(By.XPATH,
                                            f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i}]/div[3]/div[{random.randint(1, 4)}]/div[2]"
                                            ).click()
                        time.sleep(time_2)
                        try:
                            driver.find_element(By.XPATH,
                                                f"//*[@id='wrapper-learn']/div/div/div[3]/div[2]"
                                                ).click()
                        except:
                            pass
                time.sleep(time_2)
            except:
                driver.find_element(By.XPATH,
                                    f"/html/body/div[1]/div/div[1]/div[1]"
                                    ).click()
                time.sleep(1)
                driver.find_element(By.XPATH,
                                    f"//*[@id='wrapper-learn']/div[2]/div/div/div/div[5]/a[3]"
                                    ).click()
                break
    elif ch_d == 3:
        driver.find_element(By.XPATH,
                            "/html/body/div[2]/div/div[2]/div[1]/div[3]"
                            ).click()
        driver.find_element(By.CSS_SELECTOR,
                            "#wrapper-learn > div.start-opt-body > div > div > div > div.m-t > a"
                            ).click()
        time.sleep(2)
        try:
            for i in range(1, num_d):
                cash_d = driver.find_element(By.XPATH,
                                             f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i}]/div[1]/div/div/div/div[1]/span[1]"
                                             ).text
                if cash_d.upper() != cash_d.lower():
                    try:
                        text = da_k[da_e.index(cash_d)]
                    except ValueError:
                        text = da_e[da_k.index(cash_d)]
                else:
                    text = da_e[da_k.index(cash_d)]
                in_tag = driver.find_element(By.CSS_SELECTOR,
                                             "#wrapper-learn > div > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.current.showing > div.card-bottom > div > div > div > div.text-normal.spell-input > input"
                                             )
                in_tag.click()
                in_tag.send_keys(text)
                driver.find_element(By.XPATH,
                                    "//*[@id='wrapper-learn']/div/div/div[3]"
                                    ).click()
                time.sleep(1.5)
                try:
                    driver.find_element(By.XPATH,
                                        "//*[@id='wrapper-learn']/div/div/div[3]/div[2]"
                                        ).click()
                except:
                    pass
                i += 1
                time.sleep(1)
        except NoSuchElementException:
            pass
    elif ch_d == 4:
        driver.find_element(By.XPATH,
                            "/html/body/div[2]/div/div[2]/div[2]/div"
                            ).click()
        time.sleep(time_1)
        driver.find_element(By.CSS_SELECTOR,
                            "#wrapper-test > div > div.quiz-start-div > div.layer.retry-layer.box > div.m-t-xl > a"
                            ).click()
        driver.find_element(By.XPATH,
                            "//*[@id='wrapper-test']/div/div[1]/div[3]/div[3]/a"
                            ).click()
        # 이미 학습 기록이 존재한다는 알림창이 나타날 시 아래 코드 사용
        '''
        for _ in range(2):
            time.sleep(1)
            driver.find_element(By.XPATH,
                                "//*[@id='confirmModal']/div[2]/div/div[2]/a[3]"
                                ).click()
        '''
        #print(da_k)
        #print(da_e)

        for i in range(1, num_d):
            time.sleep(0.5)
            cash_d = driver.find_element(By.XPATH,
                                         f"//*[@id='testForm']/div[{i}]/div/div[1]/div[2]/div/div/div"
                                         ).text

            element = driver.find_element(By.XPATH,
                                          f"//*[@id='testForm']/div[{i}]/div/div[1]/div[2]"
                                          )
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.5)

            cash_dby = [0, 0, 0, 0, 0, 0]
            for j in range(0, 6):
                cash_dby[j] = driver.find_element(By.XPATH,
                                                  f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{j + 1}]/label/div/div"
                                                  ).text
            #print(cash_dby)

            notFindData = False
            if cash_d.upper() != cash_d.lower():
                for j in range(0, 6):
                    try:
                        if da_e.index(cash_d) == da_k.index(cash_dby[j]):
                            element = driver.find_element(By.XPATH,
                                                        f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{j + 1}]/label/div/div"
                                                        )
                            driver.execute_script("arguments[0].click();", element)
                            notFindData = True
                            break
                    except:
                        if da_e.index(cash_d) == da_kn.index(cash_dby[j]):
                            element = driver.find_element(By.XPATH,
                                                        f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{j + 1}]/label/div/div"
                                                        )
                            driver.execute_script("arguments[0].click();", element)
                            notFindData = True
                            break
            else:
                for j in range(0, 6):
                    try:
                        if da_k.index(cash_d) == da_e.index(cash_dby[j]):
                            element = driver.find_element(By.XPATH,
                                                        f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{j + 1}]/label/div/div"
                                                        )
                            driver.execute_script("arguments[0].click();", element)
                            notFindData = True
                            break
                    except:
                        if da_kn.index(cash_d) == da_e.index(cash_dby[j]):
                            element = driver.find_element(By.XPATH,
                                                        f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{j + 1}]/label/div/div"
                                                        )
                            driver.execute_script("arguments[0].click();", element)
                            notFindData = True
                            break
            if notFindData != True:
                print("\nDetected Missing Words!!, Randomly Selected\n")
                driver.find_element(By.XPATH,
                                    f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{random.randint(1, 6)}]/label/div/div"
                                    ).click()
                time.sleep(time_1)
            time.sleep(1.2)
    elif ch_d == 5:
        print("Ctrl + C 를 눌러 강제 종료")
        driver.find_element(By.XPATH,
                            "/html/body/div[2]/div/div[2]/div[1]/div[5]"
                            ).click()
        driver.find_element(By.CSS_SELECTOR,
                            "#wrapper-learn > div.vertical-mid.center.fill-parent > div.start-opt-body > div > div > div.start-opt-box > div:nth-child(4) > a"
                            ).click()
        time.sleep(1)

        time.sleep(2.5)
        past_cards = ""
        while True:
            try:
                html = BeautifulSoup(driver.page_source, "html.parser")

                unsorted_cards = dict()
                cards = html.find("div", class_="match-body").get_text(strip=True)

                if past_cards == cards:
                    raise NotImplementedError
                for i in range(4):
                    left_card = html.find("div", id="left_card_{}".format(i))
                    score = int(
                        left_card.find("span", class_="card-score").get_text(strip=True)
                    )
                    left_card.find("span", class_="card-score").decompose()
                    question = left_card.get_text(strip=True)
                    unsorted_cards["{}_{}".format(question, str(i))] = score

                    sorted_lists = {
                        k: v
                        for k, v in sorted(
                            unsorted_cards.items(), key=lambda item: item[1]
                        )
                    }.keys()
                for k in sorted_lists:
                    word = k.split("_")[0]
                    order = k.split("_")[1]
                    answer = da_k[da_e.index(word)]

                    for j in range(4):
                        right_card = html.find(
                            "div", id="right_card_{}".format(j)
                        ).get_text(strip=True)
                        if right_card == answer:
                            left_element = driver.find_element(By.ID,
                                                               "left_card_{}".format(order)
                                                               )
                            right_element = driver.find_element(By.ID,
                                                                "right_card_{}".format(j)
                                                                )
                            try:
                                left_element.click()
                                right_element.click()
                            except ElementClickInterceptedException:
                                action = ActionChains(driver)
                                action.click(on_element=left_element)
                                action.click(on_element=right_element)
                                action.perform()
                                action.reset_actions()
                            raise NotImplementedError
                        else:
                            continue
            except NotImplementedError:
                if driver.find_element(By.CLASS_NAME, "rank-info").size["height"] > 0:
                    print("완료되었습니다")
                    driver.find_element(By.CSS_SELECTOR, ".btn-default").click()
                    time.sleep(1)
                    break
                else:
                    past_cards = cards
            except KeyboardInterrupt:
                break
    elif ch_d == 6:
        driver.get('https://b.classcard.net/Home/battle_enter?u_n=')
        try:
            qb_code = driver.find_element(By.ID, "battel_id")
            qb_code.clear()
            qb_data = input("배틀코드를 입력하세요:")
            qb_code.send_keys(qb_data)
            driver.find_element(By.CSS_SELECTOR,
                                "body > div.battle-wrapper > div.battle-table > div > div > div > div.battle-content.step-join > div.input-step1.text-center > div > div:nth-child(1) > div:nth-child(5) > a"
                                ).click()
            time.sleep(1)
            qb_name = driver.find_element(By.ID, "user_name")
            qb_dname = input("이름을 입력하세요:")
            qb_name.send_keys(qb_dname)
            driver.find_element(By.CSS_SELECTOR,
                                "body > div.battle-wrapper > div.battle-table > div > div > div > div.battle-content.step-join > div.input-step1.text-center > div > div:nth-child(2) > div:nth-child(5) > button"
                                ).click()
        except:
            pass

        element = WebDriverWait(driver, 100000).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div[1]")))
        beforeCash_d = '$%(@!_'

        while True:
            bfb = str(driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[2]").get_attribute('class'))
            bah = str(driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[3]").get_attribute('class'))
            bar = str(driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[4]").get_attribute('class'))
            if bar == 'battle-result battle-rank hidden' and bah == 'battle-result battle-score animated hidden':
                if bfb == 'battle-result battle-feedback hidden':
                    time.sleep(0.2)
                    try:
                        cash_d = driver.find_element(By.XPATH,
                                                     f"/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div[1]"
                                                     ).text
                        if cash_d == '':
                            raise NoSuchElementException
                        if cash_d == beforeCash_d:
                            raise ValueError

                        cash_dby = [0, 0, 0, 0]

                        for j in range(0, 4):
                            cash_dby[j] = driver.find_element(By.XPATH,
                                                              f"/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[{j + 1}]/div/div"
                                                              ).text
                        time.sleep(0.1)
                        notFindData = False

                        if cash_d.upper() != cash_d.lower():
                            for j in range(0, 4):
                                if da_e.index(cash_d) == da_k.index(cash_dby[j]):
                                    element = driver.find_element(By.XPATH,
                                                                  f"/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[{j + 1}]/div/div"
                                                                  )
                                    driver.execute_script("arguments[0].click();", element)
                                    notFindData = True
                                    break
                        else:
                            for j in range(0, 4):
                                if da_k.index(cash_d) == da_e.index(cash_dby[j]):
                                    element = driver.find_element(By.XPATH,
                                                                  f"/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[{j + 1}]/div/div"
                                                                  )
                                    driver.execute_script("arguments[0].click();", element)
                                    notFindData = True
                                    break

                        if notFindData != True:
                            print("\nDetected Missing Words!!, Randomly Selected\n")
                            driver.find_element(By.XPATH,
                                                f"/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[{random.randint(1, 4)}]/div/div"
                                                ).click()
                            time.sleep(0.2)
                        beforeCash_d = cash_d
                        time.sleep(0.3)
                    except NoSuchElementException:
                        time.sleep(0.5)
                        cash_sd = str(driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div[1]/a").get_attribute('data-src'))

                        cash_sdy = [0, 0, 0, 0]

                        for j in range(0, 4):
                            cash_sdy[j] = driver.find_element(By.XPATH,
                                                              f"/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[{j + 1}]/div/div"
                                                              ).text
                        time.sleep(0.2)
                        notFindData = False

                        if cash_sdy[0].upper() != cash_sdy[0].lower():
                            for j in range(0, 4):
                                if da_sd.index(cash_sd) == da_e.index(cash_sdy[j]):
                                    element = driver.find_element(By.XPATH,
                                                                  f"/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[{j + 1}]/div/div"
                                                                  )
                                    driver.execute_script("arguments[0].click();", element)
                                    notFindData = True
                                    break
                        else:
                            for j in range(0, 4):
                                if da_sd.index(cash_sd) == da_k.index(cash_sdy[j]):
                                    element = driver.find_element(By.XPATH,
                                                                  f"/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[{j + 1}]/div/div"
                                                                  )
                                    driver.execute_script("arguments[0].click();", element)
                                    notFindData = True
                                    break

                        if notFindData != True:
                            print("\nDetected Missing Words!!, Randomly Selected\n")
                            driver.find_element(By.XPATH,
                                                f"/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[{random.randint(1, 4)}]/div/div"
                                                ).click()
                            time.sleep(0.2)
                        time.sleep(0.4)
                    except ValueError:
                        pass
                    time.sleep(0.2)
