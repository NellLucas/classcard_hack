# learning_types/quiz_battle.py
import time
import random
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_quiz_battle(driver, da_e, da_k, da_sd):
    print("퀴즈배틀을 시작합니다...")
    driver.get('https://b.classcard.net/Home/battle_enter?u_n=')
    time.sleep(1)
    try:
        qb_code = driver.find_element(By.ID, "battel_id")
        qb_code.clear()
        qb_data = input("Enter Battle Code: ")
        qb_code.send_keys(qb_data)
        driver.find_element(By.CSS_SELECTOR,
                            "body > div.battle-wrapper > div.battle-table > div > div > div > div.battle-content.step-join > div.input-step1.text-center > div > div:nth-child(1) > div:nth-child(5) > a"
                            ).click()
        time.sleep(1)
        qb_name = driver.find_element(By.ID, "user_name")
        qb_dname = input("Enter Your Name: ")
        qb_name.send_keys(qb_dname)
        driver.find_element(By.CSS_SELECTOR,
                            "body > div.battle-wrapper > div.battle-table > div > div > div > div.battle-content.step-join > div.input-step1.text-center > div > div:nth-child(2) > div:nth-child(5) > button"
                            ).click()
    except NoSuchElementException:
        print("Error entering Quiz Battle mode.")
        pass

    element = WebDriverWait(driver, 100000).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div[1]"))
    )
    beforeCash_d = None

    while True:
        try:
            bfb = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[2]").get_attribute('class')
            bah = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[3]").get_attribute('class')
            bar = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[4]").get_attribute('class')
            
            if bar == 'battle-result battle-rank hidden' and bah == 'battle-result battle-score animated hidden':
                if bfb == 'battle-result battle-feedback hidden':
                    time.sleep(0.2)
                    try:
                        cash_d = driver.find_element(By.XPATH,
                                                     "/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div[1]"
                                                     ).text
                        if not cash_d:
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
                        cash_sd = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div/div/div[4]/div[3]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div[1]/a").get_attribute('data-src')

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
        except KeyboardInterrupt:
            print("\nQuiz Battle이 사용자에 의해 종료되었습니다.")
            break
    print("Quiz Battle이 완료되었습니다.")
