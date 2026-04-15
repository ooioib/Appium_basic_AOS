# 3_basic.py

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from base import AppiumConnection


class Uiautomatortest(AppiumConnection):

    def examTest(self):
        try:
            print("요소를 기다리는 중...")

            # API Demos 클릭
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (AppiumBy.ACCESSIBILITY_ID, "API Demos")
                )
            ).click()

            # Views 클릭
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().text("Views")'
                    )
                )
            ).click()

            # 클릭 가능한 요소 개수 확인
            clickable = self.driver.find_elements(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().clickable(true)'
            )

            print(f"클릭 가능한 요소 수: {len(clickable)}")
            print("요소 테스트 완료!")

        except TimeoutException:
            print("요소를 찾는 데 시간이 초과되었습니다.")

        except Exception as e:
            print("요소 테스트 중 오류 발생:", e)


if __name__ == "__main__":
    automation = Uiautomatortest()
    automation.connect()

    if automation.driver:
        automation.examTest()

    automation.quit()