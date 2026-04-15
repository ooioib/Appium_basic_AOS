# practice_1.py

# =============================================================================
# 목적: Appium을 활용한 Android 모바일 앱 자동화 테스트 스크립트
# 대상 앱: YouTube, Gmail (기본 설치 앱)
# 테스트 시나리오:
#   1) YouTube 앱 실행 → 검색 → 영상 선택 → 광고 스킵 처리
#   2) Gmail 앱 정보 확인 (롱 클릭 → App Info 진입)
# 환경: Android 디바이스 + Appium 서버 기반
# =============================================================================

# AppiumConnection 클래스가 정의된 파일을 가져오기
import time
from appium.webdriver.common.appiumby import AppiumBy          # Appium 전용 요소 탐색 방식 (XPATH 등)
from selenium.webdriver.support.ui import WebDriverWait        # 특정 요소가 나타날 때까지 대기
from selenium.webdriver.support import expected_conditions as EC  # 대기 조건 정의 (요소 존재, 클릭 가능 등)
from selenium.common.exceptions import TimeoutException        # 대기 시간 초과 시 발생하는 예외

# Appium 서버 연결/해제 등 공통 기능을 담당하는 base 클래스
from base import AppiumConnection

# YouTube 검색·재생 및 Gmail 앱 정보 확인을 자동화하는 테스트 클래스
class AppAutomation(AppiumConnection):

    # ── 메인 테스트 함수 ──
    # 검증 항목:
    #   - YouTube 앱 정상 실행 여부
    #   - 검색 기능 동작 여부 (키 입력 → 검색 실행)
    #   - 검색 결과 화면에서 영상 선택 가능 여부
    #   - 광고 스킵 버튼 존재 시 정상 클릭 여부
    #   - Gmail 롱 클릭 → 앱 정보 화면 진입 여부
    def examTest(self):
        try:
            print(f"요소를 기다리는 중...")
            # [STEP 1] YouTube 앱 실행
            # 홈 화면에서 "YouTube" 아이콘을 찾아 탭한다.
            # //android.widget.TextView[@content-desc="YouTube"]
            self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="YouTube"]').click()


            # [STEP 2] 검색 버튼 있는 경우 클릭
            # YouTube 앱 상단의 돋보기(Search) 아이콘이 나타날 때까지 최대 10초 대기 후 클릭
            # //android.widget.ImageView[@content-desc="Search"]
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="Search"]'))
            ).click()

            # [STEP 3] 검색어 "RPA test" 입력
            # send_keys()가 정상 동작하지 않는 환경을 대비하여 press_keycode를 사용해 한 글자씩 직접 입력

            # //android.view.ViewGroup[@content-desc="Search YouTube"]
            # //android.widget.LinearLayout[@resource-id="com.google.android.youtube:id/search_box"]
            # //android.widget.EditText[@resource-id="com.google.android.youtube:id/search_edit_text"]            
            time.sleep(5)
            # self.driver.find_element(by=AppiumBy.CLASS_NAME, value='//android.widget.LinearLayout[@resource-id="com.google.android.youtube:id/search_box"]').send_keys("RPA test")
            # self.driver.switch_to.active_element.send_keys("RPA test")
            self.driver.press_keycode(46)  # R
            self.driver.press_keycode(44)  # P
            self.driver.press_keycode(29)  # A
            self.driver.press_keycode(62)  # SPACE
            self.driver.press_keycode(48)  # T
            self.driver.press_keycode(33)  # E
            self.driver.press_keycode(47)  # S
            self.driver.press_keycode(48)  # T

            # [STEP 4] 검색 버튼 클릭 (엔터 키 입력)
            # press_keycode(66)
            self.driver.press_keycode(66)

            # [STEP 5] 검색 결과에서 영상 선택
            # 검색 결과 로딩을 위해 5초 대기 후,
            # "Navigate up" 버튼의 좌표를 기준점으로 삼아 오프셋을 적용하여 영상 썸네일 위치를 클릭
            # //android.widget.ImageButton[@content-desc="Navigate up"]
            time.sleep(5)

            # 기준 요소("Navigate up" 버튼)의 위치·크기 정보를 가져옴
            # self.driver.find_element(by=AppiumBy.XPATH, value='//android.view.ViewGroup[@content-desc="RPA vs. Test Automation (3 key differences!) - 3 minutes, 47 seconds - Go to channel - What is RPA - 295 views - 2 years ago - play video"]/android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.ImageView').click()
            element = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Navigate up"]')
            rect = element.rect  # 요소의 위치와 크기 정보 가져오기

            # 기준 요소의 중심 좌표 계산
            center_x = rect['x'] + rect['width'] / 2
            center_y = rect['y'] + rect['height'] / 2

            # 기준점에서 오프셋을 적용하여 실제 클릭할 영상 위치를 산출
            adjusted_x = center_x + 200
            adjusted_y = center_y + 300

            # Appium의 W3C 제스처 API를 사용하여 계산된 좌표를 클릭
            self.driver.execute_script('mobile: clickGesture', {
                'x': center_x,
                'y': adjusted_y
            })
            
            # [STEP 6] 광고 스킵 처리
            # 영상 재생 시 광고가 표시될 수 있으므로, "광고 건너뛰기" 버튼 존재 여부를 확인한다.
            # - 버튼이 있으면 → 클릭하여 광고를 건너뛴다.
            # - 버튼이 없으면 → 홈 버튼을 눌러 테스트 흐름을 이어간다.
            # find_elements()는 요소가 없어도 예외를 발생시키지 않고 빈 리스트를 반환한다.
            # time.sleep(5)
            # //android.widget.TextView[@resource-id="com.google.android.youtube:id/skip_ad_button_text"]
            # WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.google.android.youtube:id/skip_ad_button_text"]'))
            # ).click()
            elements = self.driver.find_elements(
                by=AppiumBy.XPATH,
                value='//android.widget.TextView[@resource-id="com.google.android.youtube:id/skip_ad_button_text"]'
            )

            if elements:
                elements[0].click()
                print("광고 스킵 버튼 클릭 완료")
            else:
                print("홈 버튼 클릭")
                # 6. 유투브 아이콘이 보일 때까지 백 버튼 클릭
                # self.driver.press_keycode(4)
                # or 홈 버튼 클릭
                # press_keycode(3)  # KEYCODE_HOME
                self.driver.press_keycode(3)           

            # 7. Gmail 아이콘 롱 클릭
            # //android.widget.TextView[@content-desc="Gmail"]
            # 대상 요소의 좌표 가져오기
            time.sleep(5)
            element = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Gmail"]')
            rect = element.rect  # 요소의 위치와 크기 정보 가져오기

            # 요소 중심 좌표 계산
            center_x = rect['x'] + rect['width'] / 2
            center_y = rect['y'] + rect['height'] / 2

            # Appium의 'longClickGesture' 사용
            self.driver.execute_script('mobile: longClickGesture', {
                'x': center_x,
                'y': center_y,
                'duration': 2000  # LongPress 지속 시간 (밀리초, 예: 2000ms = 2초)
            })
            
            # 8. "App Info" 클릭
            # //android.widget.TextView[@resource-id="com.google.android.apps.nexuslauncher:id/bubble_text" and @text="App info"]
            time.sleep(5)
            self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="com.google.android.apps.nexuslauncher:id/bubble_text" and @text="App info"]').click()
            
            # 9. "back" 버튼 클릭
            self.driver.press_keycode(4)

            print(f"요소 테스트 완료!")
        except TimeoutException:
            print(f"요소를 찾는 데 시간이 초과되었습니다.")
        except Exception as e:
            print(f"요소 테스트 중 오류 발생: {e}")

# =============================================================================
# ── 실행 진입점 (Entry Point) ──
# 이 파일을 직접 실행할 때만 아래 코드가 동작한다.
# 흐름: Appium 서버 연결 → 테스트 실행 → 연결 종료
# =============================================================================
if __name__ == "__main__":
    # Appium 드라이버 인스턴스 생성
    automation = AppAutomation()
    # Appium 서버에 연결 (디바이스 세션 시작)
    automation.connect()
 
    # 드라이버가 정상 연결된 경우에만 테스트 실행
    if automation.driver:
        # 예: "com.example:id/button_start" 리소스 ID를 가진 버튼 클릭
        automation.examTest()
    
    # 테스트 종료 후 Appium 세션 및 드라이버 정리
    automation.quit()