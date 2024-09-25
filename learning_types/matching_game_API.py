import time
import requests
from urllib.parse import quote

class ggk:
    def __init__(self, key_array):
        self.k = key_array

    def c(self, a):
        r = ""
        a = str(a)
        for ii in a:
            if ii == ".":
                r += "."
                continue
            try:
                idx = int(ii)
            except ValueError:
                continue
            if idx < len(self.k):
                r += self.k[idx]
        return r

    def hack(self, time_val, score):
        return {
            't': self.c(time_val / 1000),
            's': self.c(score),
            'm': self.c(1)
        }

def run_matching_game_api(driver, match_site):
    time.sleep(1.5)
    tid = driver.execute_script('return window.tid;')
    set_idx = driver.execute_script('return window.set_idx;')
    class_idx = driver.execute_script('return window.class_idx;')
    cookies = "; ".join([f"{c['name']}={c['value']}" for c in driver.get_cookies()])

#-----------options-------------
    count = 8000
    interval = 2
#-----------options-------------    

    activity = 4
    start_time = int(time.time() * 1000)

    arr_key = driver.execute_script('return ggk.a();')
    ggk_instance = ggk(arr_key)
    arr_score = [ggk_instance.hack(start_time + i * interval, 130) for i in range(count)]

    encodedDataArray = []
    encodedDataArray.append(f"set_idx={set_idx}")
    for key in arr_key:
        encodedDataArray.append(f"arr_key%5B%5D={key}")
    for index, score in enumerate(arr_score):
        encodedDataArray.append(f"arr_score%5B{index}%5D%5Bt%5D={quote(score['t'])}")
        encodedDataArray.append(f"arr_score%5B{index}%5D%5Bs%5D={quote(score['s'])}")
        encodedDataArray.append(f"arr_score%5B{index}%5D%5Bm%5D={quote(score['m'])}")
    encodedDataArray.append(f"activity={activity}")
    encodedDataArray.append(f"tid={tid}")
    encodedDataArray.append(f"class_idx={class_idx}")

    #print(encodedDataArray)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": match_site,
        "Origin": "https://classcard.net",
        "Cookie": cookies,
    }


    try:
        response = requests.post("https://www.classcard.net/Match/save", headers=headers, data="&".join(encodedDataArray))
        response.raise_for_status()
        data = response.json()
        print("조작된 페이로드가 성공적으로 전송되었습니다.")
        print("응답 데이터:", data)
    except requests.exceptions.RequestException as e:
        print("페이로드 전송 중 오류가 발생했습니다:", e)
    except ValueError:
        print("서버로부터 유효한 JSON 응답을 받지 못했습니다.")
