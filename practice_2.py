from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# AppiumConnection 클래스 가져오기
from base import AppiumConnection


class HybridAppDemo(AppiumConnection):

    def examTest(self):
        try:
            print("GeneralStore 앱 실행 중...")

            # 기존 앱 종료 후 재실행
            self.driver.terminate_app("com.androidsample.generalstore")
            time.sleep(1)

            self.driver.activate_app("com.androidsample.generalstore")
            time.sleep(3)

            print("GeneralStore 앱 실행 완료")

            wait = WebDriverWait(self.driver, 15)

            # -----------------------------
            # 1. 이름 입력
            # -----------------------------
            name_box = wait.until(
                EC.presence_of_element_located(
                    (AppiumBy.CLASS_NAME, "android.widget.EditText")
                )
            )
            name_box.send_keys("Hello")

            # -----------------------------
            # 2. Let's Shop 클릭
            # -----------------------------
            wait.until(
                EC.element_to_be_clickable(
                    (AppiumBy.ID,
                     "com.androidsample.generalstore:id/btnLetsShop")
                )
            ).click()

            # -----------------------------
            # 3. 상품 담기
            # -----------------------------
            wait.until(
                EC.element_to_be_clickable(
                    (AppiumBy.XPATH,
                     '//*[@text="ADD TO CART"]')
                )
            ).click()

            # -----------------------------
            # 4. 장바구니 이동
            # -----------------------------
            wait.until(
                EC.element_to_be_clickable(
                    (AppiumBy.ID,
                     "com.androidsample.generalstore:id/appbar_btn_cart")
                )
            ).click()

            time.sleep(2)

            # -----------------------------
            # 5. 체크박스 클릭
            # -----------------------------
            wait.until(
                EC.element_to_be_clickable(
                    (AppiumBy.CLASS_NAME,
                     "android.widget.CheckBox")
                )
            ).click()

            # -----------------------------
            # 6. 약관 롱클릭
            # -----------------------------
            terms = wait.until(
                EC.presence_of_element_located(
                    (AppiumBy.XPATH,
                     '//*[@text="Please read our terms of conditions"]')
                )
            )

            rect = terms.rect
            x = rect["x"] + rect["width"] / 2
            y = rect["y"] + rect["height"] / 2

            self.driver.execute_script(
                "mobile: longClickGesture",
                {
                    "x": x,
                    "y": y,
                    "duration": 2000
                }
            )

            # -----------------------------
            # 7. 팝업 닫기
            # -----------------------------
            wait.until(
                EC.element_to_be_clickable(
                    (AppiumBy.ID, "android:id/button1")
                )
            ).click()

            # -----------------------------
            # 8. 웹사이트 이동
            # -----------------------------
            wait.until(
                EC.element_to_be_clickable(
                    (AppiumBy.ID,
                     "com.androidsample.generalstore:id/btnProceed")
                )
            ).click()

            print("웹뷰 로딩 대기 중...")
            time.sleep(8)

            # -----------------------------
            # 9. 컨텍스트 확인
            # -----------------------------
            contexts = self.driver.contexts
            print("사용 가능한 컨텍스트:", contexts)

            # WEBVIEW 찾기
            webview = None
            for ctx in contexts:
                if "WEBVIEW" in ctx:
                    webview = ctx
                    break

            if webview:
                self.driver.switch_to.context(webview)
                print("WEBVIEW 전환 완료:", webview)
            else:
                print("WEBVIEW 없음")
                return

            time.sleep(3)

            # -----------------------------
            # 10. 검색창 입력
            # -----------------------------
            search_box = wait.until(
                EC.presence_of_element_located(
                    (By.NAME, "q")
                )
            )

            search_box.send_keys("codenbox")
            search_box.send_keys(Keys.ENTER)

            print("검색 완료!")
            print("전체 테스트 완료!")

        except TimeoutException:
            print("요소를 찾는 데 시간이 초과되었습니다.")

        except Exception as e:
            print(f"오류 발생: {e}")

        finally:
            print("드라이버를 종료합니다...")
            self.driver.quit()
            print("드라이버가 종료되었습니다.")


if __name__ == "__main__":
    automation = HybridAppDemo()
    automation.connect()

    if automation.driver:
        automation.examTest()