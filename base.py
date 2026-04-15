# base.py

import time
from appium import webdriver
from appium.options.common.base import AppiumOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AppiumConnection:
    def __init__(self):
        self.driver = None

        # Appium 옵션 설정
        self.options = AppiumOptions()
        self.options.load_capabilities({
            # 기본 설정
            "appium:automationName": "UiAutomator2",
            "appium:platformName": "Android",
            "appium:deviceName": "emulator-5554",
            "appium:platformVersion": "14",

            # 기존 옵션
            "appium:settings[enableMultiWindows]": True,
            "appium:wdaLocalPort": "8100",
            "appium:settings[allowInvisibleElements]": True,
            "appium:connectHardwareKeyboard": True,

            # 세션 유지
            "appium:noReset": True,
            "appium:newCommandTimeout": 300,

            # Hybrid App 핵심 옵션 (추가)
            "appium:chromedriverAutodownload": True,
            "appium:autoWebview": False,

            # 권한 자동 허용
            "appium:autoGrantPermissions": True
        })

    def connect(self):
        try:
            print("Appium 서버 연결 시도 중...")
            self.driver = webdriver.Remote(
                "http://127.0.0.1:4723",
                options=self.options
            )
            print("Appium 서버 연결 성공!")

        except Exception as e:
            print(f"Appium 서버 연결 실패: {e}")

    def quit(self):
        if self.driver:
            print("드라이버를 종료합니다...")
            self.driver.quit()
            print("드라이버가 종료되었습니다.")


# 사용 예시
if __name__ == "__main__":
    appium_connection = AppiumConnection()
    appium_connection.connect()

    if appium_connection.driver:
        try:
            WebDriverWait(appium_connection.driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "com.example:id/sampleElement")
                )
            )
            print("요소를 성공적으로 찾았습니다!")

        except TimeoutException:
            print("요소를 찾는 데 시간이 초과되었습니다.")

    appium_connection.quit()