
"""
    사용 예시
    crawler = IMDBMovieCrawler(country_codes_filepath='./data/raw/country_code.json', top_n=10)
    crawler.crawling()
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from tqdm import tqdm
from datetime import datetime


class IMDBMovieCrawler:
    def __init__(self, country_codes_filepath='./data/raw/country_code.json', top_n=10):
        """
        크롤러 초기화 함수

        :param country_codes_filepath: 국가 코드가 저장된 JSON 파일 경로
        :param top_n: 크롤링할 영화의 수
        """
        self.BASE_URL = 'https://www.imdb.com/search/title/?countries={}'
        self.BASE_XPATH = '/html/body/div[4]/div[2]/div/div[2]/div/div'
        self.RELATIVE_XPATHS = {
            'img': '/div[1]/div[1]/div/div/img',
            'title': '/div[1]/div[2]/div[1]/a/h3',
            'year': '/div[1]/div[2]/ul[1]/li[1]',
            'score': '/div[1]/div[2]/div[2]/span/span[1]',
            'summary': '/div[2]'
        }
        self.ELEMENTS_PATH = {
            'genre': '/div[1]/div[2]/ul[2]/li[{}]',
            'stars': '/div[3]/div/ul/li[{}]'
        }
        self.CLOSE_BUTTON_XPATH = '/html/body/div[4]/div[2]/div/div[1]/button'
        self.BUTTON_XPATH_TEMPLATE = (
            '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/'
            'div[2]/div[2]/ul/li[{}]/div/div/div/div[1]/div[3]/button'
        )
        self.country_codes_filepath = country_codes_filepath
        self.top_n = top_n

    def load_country_codes(self):
        """
        국가 코드 JSON 파일을 로드하는 함수
        
        :return: 국가 코드 딕셔너리
        """
        with open(self.country_codes_filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    def initialize_driver(self):
        """
        Chrome WebDriver를 초기화하는 함수
        
        :return: 초기화된 WebDriver 인스턴스
        """
        options = self.configure_chrome_options()
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def configure_chrome_options(self):
        """
        Chrome WebDriver 옵션을 설정하는 함수
        
        :return: 설정된 ChromeOptions 객체
        """
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')  # 필요시 headless 모드 활성화
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        return options

    def click_button(self, driver, wait, xpath: str):
        """
        주어진 XPATH로 버튼을 클릭하는 함수

        :param driver: Selenium WebDriver 인스턴스
        :param wait: WebDriverWait 인스턴스 (타임아웃 설정)
        :param xpath: 클릭할 버튼의 XPATH
        """
        button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        ActionChains(driver).click(button).perform()

    def scrape_modal_content(self, wait, base_xpath: str, relative_xpaths: dict) -> dict:
        """
        모달 창에서 콘텐츠를 추출하는 함수

        :param wait: WebDriverWait 인스턴스 (타임아웃 설정)
        :param base_xpath: 모든 요소에 공통으로 사용되는 XPATH
        :param relative_xpaths: 각 요소별 상대적인 XPATH가 담긴 딕셔너리
        :return: 추출된 콘텐츠(img_url, 제목, 개봉년도, 평점, 요약)가 담긴 딕셔너리
        """
        extracted_content = {}
        for element_name, relative_xpath in relative_xpaths.items():
            try:
                full_xpath = base_xpath + relative_xpath
                if element_name == 'img':
                    # 이미지의 경우 'src' 속성을 가져옴
                    extracted_content[element_name] = wait.until(
                        EC.presence_of_element_located((By.XPATH, full_xpath))
                    ).get_attribute('src')
                else:
                    # 나머지 요소는 텍스트를 가져옴
                    extracted_content[element_name] = wait.until(
                        EC.presence_of_element_located((By.XPATH, full_xpath))
                    ).text
            except Exception as e:
                print(f"Error fetching {element_name}: {e}")
        return extracted_content

    def scrape_modal_data(self, driver, base_xpath: str, relative_xpaths: dict) -> dict:
        """
        모달 창에서 반복적으로 나타나는 데이터를 추출하는 함수

        :param driver: Selenium WebDriver 인스턴스
        :param base_xpath: 모든 요소에 공통으로 사용되는 XPATH
        :param relative_xpaths: 각 요소별 상대적인 XPATH 템플릿이 담긴 딕셔너리
        :return: 추출된 데이터(장르 리스트, 출연진 리스트) 가 담긴 딕셔너리
        """
        extracted_data = {}
        # 상대 XPATH 템플릿을 기준으로 반복
        for element_name, xpath_template in relative_xpaths.items():
            values = []
            index = 1
            while True:
                try:
                    full_xpath = f"{base_xpath}{xpath_template.format(index)}"
                    element = driver.find_element(By.XPATH, full_xpath)
                    values.append(element.text)
                    index += 1
                except Exception:
                    break
            # 추출한 값들을 딕셔너리에 저장 (키는 element_name, 값은 values 리스트)
            extracted_data[element_name] = values
        return extracted_data

    def log_error(self, country, rank, error):
        """
        에러 발생 시 로그를 기록하는 함수
        
        :param country: 영화가 속한 국가
        :param rank: 영화의 순위
        :param error: 발생한 예외
        """
        print(f"Error processing item {rank} for {country}: {error}")

    def save_dict_as_json(self, data, file_path):
        """
        딕셔너리 데이터를 JSON 파일로 저장하는 함수
        
        :param data: 저장할 데이터 (딕셔너리)
        :param file_path: 저장할 파일 경로
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("JSON 파일이 성공적으로 저장되었습니다!")
        except Exception as e:
            print(f"An error occured:{e}")

    def transform_content_to_result(self, content: dict, country: str) -> dict:
        """
        추출한 콘텐츠를 요구되는 JSON 구조로 변환하는 함수

        :param content: 추출된 콘텐츠 (딕셔너리)
        :param country: 영화가 속한 국가
        :return: 변환된 JSON 구조
        """
        return {
            "country": country,
            "movie": {
                "title": content.get("title"),
                "release_year": content.get("year"),
                "score": content.get("score"),
                "summary": content.get("summary"),
                "image_url": content.get("img"),
                "genres": content.get("genre", []),
                "actors": content.get("stars", [])
            },
            "rank": content["rank"]
        }

    def process_movie(self, driver, wait, country, country_code, rank):
        """
        단일 영화 항목을 처리하는 함수

        :param driver: Selenium WebDriver 인스턴스
        :param wait: WebDriverWait 인스턴스 (타임아웃 설정)
        :param country: 영화가 속한 국가
        :param country_code: 국가 코드
        :param rank: 영화의 순위
        :return: 추출된 영화 정보가 담긴 딕셔너리
        """
        content = {}
        try:
            print(f"Processing item {rank} for {country}({country_code})")
            # 버튼 클릭
            button_xpath = BUTTON_XPATH_TEMPLATE.format(rank)
            click_button(driver, wait, button_xpath)
            time.sleep(0.5)
            # 콘텐츠 크롤링 -> img_url, 제목, 개봉년도, 평점, 요약
            content = scrape_modal_content(wait, BASE_XPATH, RELATIVE_XPATHS)
            # 국가 추가
            content['country'] = country
            # 추가 데이터 -> 장르, 출연진
            content.update(scrape_modal_data(driver, BASE_XPATH, ELEMENTS_PATH))
            # 순위 추가
            content['rank'] = rank
            # 모달 닫기
            click_button(driver, wait, CLOSE_BUTTON_XPATH)
            time.sleep(0.5)
        except Exception as e:
            self.log_error(country, rank, e)
        return content

    def crawling(self):
        """
        메인 크롤링 함수

        :return: 크롤링한 영화 정보가 담긴 딕셔너리
        """
        result = {"movies": []}
        country_code_dict = self.load_country_codes()
        today_date = str(datetime.today()).replace('-', '')[:8]

        # 국가 코드 딕셔너리에서 각 국가에 대해 반복 (각 국가별로 영화 데이터를 크롤링)
        for country_code, country in tqdm(country_code_dict.items(), desc="Processing Countries"):
            with self.initialize_driver() as driver:
                wait = WebDriverWait(driver, 10)
                # 국가별 URL을 형성하여 해당 페이지로 이동
                country_url = self.BASE_URL.format(country_code)
                driver.get(country_url)

                for i in range(1, self.top_n + 1):
                    content = self.process_movie(driver, wait, country, country_code, i)
                    if content:
                        # 반환된 콘텐츠를 요구되는 JSON 구조로 변환하여 결과에 추가
                        result["movies"].append(self.transform_content_to_result(content, country))
            #결과를 파일로 저장
            save_at = f'./data/raw/movies_data_{today_date}.json'
            self.save_dict_as_json(result, save_at)
        return result
