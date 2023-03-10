import sys
from PyQt5.QtWidgets import *
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.setGeometry(200, 200, 800, 500)

        self.url_list = []

        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(600, 400)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        labels = ["url"]
        self.tableWidget.setHorizontalHeaderLabels(labels)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        btn = QPushButton(text="파일 열기", parent=self)
        btn.move(600, 0)
        btn.clicked.connect(self.fileopen)

        btn2 = QPushButton(text="캡쳐", parent=self)
        btn2.move(600, 100)
        btn2.clicked.connect(self.screenshot)

        btn3 = QPushButton(text="로그인", parent=self)
        btn3.move(600, 200)
        btn3.clicked.connect(self.daum_login)

        self.line_edit = QLineEdit("ID", self)
        self.line_edit.move(0, 400)
        self.line_edit.resize(400, 50)

        self.line_edit2 = QLineEdit("Password", self)
        self.line_edit2.move( 0,450)
        self.line_edit2.resize(400, 50)

    def screenshot(self):
        for i, url in enumerate(self.url_list):
            self.driver.get(url)
            sleep(2)
            self.driver.maximize_window()
            width = 1280
            # width = self.driver.execute_script(
            #     "return document.body.scrollWidth"
            # )  # 스크롤 할 수 있는 최대 넓이
            height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )  # 스크롤 할 수 있는 최대 높이
            if "cafe.daum" in url:
                self.driver.switch_to.frame("down")
                height = self.driver.execute_script(
                    'return document.getElementById("wrap").scrollHeight'
                )
                print("height", height)

            self.driver.set_window_size(width, height)  # 스크롤 할 수 있는 모든 부분을 지정
            self.driver.save_screenshot(f".\\screenshots\\{i}.png")
            print(url)

    def fileopen(self):
        self.url_list = []
        f = open("urls.txt", "r")
        row = 0
        while True:
            self.tableWidget.setRowCount(row + 1)
            line = f.readline()
            if not line:
                break
            self.url_list.append(line)
            self.tableWidget.setItem(0, row, QTableWidgetItem(line))
            row += 1

        f.close()
        print(self.url_list)

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


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
