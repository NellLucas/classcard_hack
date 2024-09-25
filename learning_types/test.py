# learning_types/test.py
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def wait_and_click(driver, by, identifier, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, identifier))
        )
        driver.execute_script("arguments[0].click();", element)
        return True
    except TimeoutException:
        print(f"요소를 찾는 데 시간이 초과되었습니다: {identifier}")
        return False

def wait_for_element(driver, by, identifier, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, identifier))
        )
        return element
    except TimeoutException:
        print(f"요소를 찾는 데 시간이 초과되었습니다: {identifier}")
        return None

def run_test(driver, num_d, da_e, da_k, da_kn, da_ked, time_1):
    print("테스트학습을 시작합니다...")

    initial_steps = [
        (By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div"),
        (By.CSS_SELECTOR, "#wrapper-test > div > div.quiz-start-div > div.layer.retry-layer.box > div.m-t-xl > a"),
        (By.XPATH, "//*[@id='wrapper-test']/div/div[1]/div[3]/div[3]/a")
    ]

    for by, identifier in initial_steps:
        if not wait_and_click(driver, by, identifier, time_1):
            print("로딩 중 문제가 발생하여 테스트학습을 종료합니다.")
            return
        time.sleep(0.7)

    for _ in range(2):
        if not wait_and_click(driver, By.XPATH, "//*[@id='confirmModal']/div[2]/div/div[2]/a[3]", timeout=1):
            break
        time.sleep(0.7)

    if not wait_for_element(driver, By.XPATH, "//*[@id='testForm']/div[1]/div/div[1]/div[2]/div/div/div", timeout=time_1):
        print("화면 전환이 완료되지 않았습니다. 테스트학습을 종료합니다.")
        return
    
    for i in range(1, num_d):
        time.sleep(0.2)
        try:
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
                        try:
                            if da_e.index(cash_d) == da_kn.index(cash_dby[j]):
                                element = driver.find_element(By.XPATH,
                                                            f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{j + 1}]/label/div/div"
                                                            )
                                driver.execute_script("arguments[0].click();", element)
                                notFindData = True
                                break
                        except:
                            if da_e.index(cash_d) == da_ked.index(cash_dby[j]):
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
                        try:
                            if da_kn.index(cash_d) == da_e.index(cash_dby[j]):
                                element = driver.find_element(By.XPATH,
                                                            f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{j + 1}]/label/div/div"
                                                            )
                                driver.execute_script("arguments[0].click();", element)
                                notFindData = True
                                break
                        except:
                            if da_ked.index(cash_d) == da_e.index(cash_dby[j]):
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
            time.sleep(1.5)
        except NoSuchElementException:
            print("단어가 더 이상 존재하지 않습니다. 테스트학습을 종료하는 중입니다...")
            break
    print("테스트학습이 완료되었습니다.")
