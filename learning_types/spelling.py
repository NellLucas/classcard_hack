# learning_types/spelling.py
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def run_spelling(driver, num_d, da_e, da_k):
    print("스펠학습을 시작합니다...")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[3]").click()
    driver.find_element(By.CSS_SELECTOR, "#wrapper-learn > div.start-opt-body > div > div > div > div.m-t > a").click()
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
            time.sleep(1)
    except NoSuchElementException:
        print("모든 단어가 학습되었습니다.")
    print("스펠학습이 완료되었습니다.")
