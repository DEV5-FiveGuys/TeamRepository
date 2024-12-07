from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os
from datetime import datetime

class MovieCrawler:
    def __init__(self, top_n=10):
        self.BASE_URL = 'https://www.imdb.com/search/title/?countries={}'
        self.BASE_XPATH = '/html/body/div[4]/div[2]/div/div[2]/div/div'
        self.RELATIVE_XPATHS = {
            'img': '/div[1]/div[1]/div/div/img',
            'title': '/div[1]/div[2]/div[1]/a/h3',
            'year': '/div[1]/div[2]/ul[1]/li[1]',
            'score': '/div[1]/div[2]/div[2]/span/span[1]',
            'summary': '/div[2]'
        }
        self.CLOSE_BUTTON_XPATH = '/html/body/div[4]/div[2]/div/div[1]/button'
        self.BUTTON_XPATH_TEMPLATE = (
            '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/'
            'div[2]/div[2]/ul/li[{}]/div/div/div/div[1]/div[3]/button'
        )
        self.top_n = top_n
        
    def load_country_codes(self, filepath='./crawler/data/raw/country_code.json'):
        """국가 코드 로드"""
        if not os.path.exists(filepath):
            print(f"{filepath} 파일이 존재하지 않습니다. 기본 데이터를 생성합니다.")
            self.create_default_country_code_file(filepath)

        # 파일을 열고 데이터를 로드
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
        
    def create_default_country_code_file(self, filepath: str ='./crawler/data/raw/country_code.json'):
        """기본 국가 코드 데이터를 json 파일로 생성하는 함수."""
        # 기본 국가 코드 데이터
        default_data = {
            "KR": "South Korea",
            "US": "United States",
            "GB": "United Kingdom",
            "AU": "Australia",
            "BR": "Brazil",
            "ZA": "South Africa"
        }

        # 디렉토리 생성 (경로에 디렉토리가 없으면 생성)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # 기본 데이터를 파일로 작성
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)
        
        print(f"기본 국가 코드 파일이 {filepath}에 생성되었습니다.")
    

    def initialize_driver(self):
        """WebDriver 초기화"""
        options = self.configure_chrome_options()
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def configure_chrome_options(self):
        """Chrome 옵션 설정"""
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        return options

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
            button_xpath = self.BUTTON_XPATH_TEMPLATE.format(rank)
            self.click_button(driver, wait, button_xpath)
            time.sleep(0.5)
            # 콘텐츠 크롤링 -> img_url, 제목, 개봉년도, 평점, 요약
            content = self.scrape_modal_content(wait, self.BASE_XPATH, self.RELATIVE_XPATHS)
            # 국가 추가
            content['country'] = country
            # 추가 데이터 -> 장르, 출연진
            content.update(self.scrape_modal_data(driver, self.BASE_XPATH, self.ELEMENTS_PATH))
            # 순위 추가
            content['rank'] = rank
            # 모달 닫기
            self.click_button(driver, wait, self.CLOSE_BUTTON_XPATH)
            time.sleep(0.5)
        except Exception as e:
            self.log_error(country, rank, e)
        return content
    
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

    def crawling(self):
        """크롤링 메인 함수"""
        result = {"movies": []}
        country_code_dict = self.load_country_codes()
        today_date = str(datetime.today()).replace('-', '')[:8]

        for country_code, country in country_code_dict.items():
            with self.initialize_driver() as driver:
                wait = WebDriverWait(driver, 10)
                country_url = self.BASE_URL.format(country_code)
                driver.get(country_url)

                for i in range(1, self.top_n + 1):
                    content = self.process_movie(driver, wait, country, country_code, i)
                    if content:
                        result["movies"].append(self.transform_content_to_result(content, country))

            save_at = f'./data/raw/movies_data_{today_date}.json'
            self.save_dict_as_json(result, save_at)
        return result
