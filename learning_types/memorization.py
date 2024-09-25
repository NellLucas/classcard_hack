# learning_types/memorization.py
import time
from selenium.webdriver.common.by import By

def run_memorization(driver, num_d):
    print("암기학습을 시작합니다...")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "#wrapper-learn > div.start-opt-body > div > div > div > div.m-t > a").click()
    
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
            print("암기할 카드가 더 이상 존재하지 않습니다.")
            break
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,
                        "body > div.study-header-body > div > div:nth-child(1) > div:nth-child(1) > a"
                        ).click()
    print("암기학습이 완료되었습니다.")
