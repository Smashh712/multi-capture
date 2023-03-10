from time import sleep
from selenium.webdriver.common.by import By

def daum_login(self):
    url = "https://accounts.kakao.com/login/?continue=https%3A%2F%2Flogins.daum.net%2Faccounts%2Fksso.do%3Frescue%3Dtrue%26url%3Dhttps%253A%252F%252Fwww.daum.net#login"
    self.driver.get(url)
    sleep(1)

    user_id = self.line_edit.text()
    user_passwd = self.line_edit2.text()

    print(f"{user_id} : id")
    print(f"{user_passwd} : pass")
    id_form = self.driver.find_element(By.XPATH, '//*[@id="loginKey--1"]')
    id_form.send_keys(user_id)

    pass_form = self.driver.find_element(By.XPATH, '//*[@id="password--2"]')
    pass_form.send_keys(user_passwd)
    id_form.submit()
    # pass_form.submit()