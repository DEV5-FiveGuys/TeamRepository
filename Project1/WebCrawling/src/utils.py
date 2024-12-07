from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json 
from utils import *
from tqdm import tqdm
from tqdm import tqdm
from datetime import datetime



# 전역 상수 정의
BASE_URL = 'https://www.imdb.com/search/title/?countries={}'
BASE_XPATH = '/html/body/div[4]/div[2]/div/div[2]/div/div'
RELATIVE_XPATHS = {
    'img': '/div[1]/div[1]/div/div/img',
    'title': '/div[1]/div[2]/div[1]/a/h3',
    'year': '/div[1]/div[2]/ul[1]/li[1]',
    'score': '/div[1]/div[2]/div[2]/span/span[1]',
    'summary': '/div[2]'
}
ELEMENTS_PATH = {
    'genre': '/div[1]/div[2]/ul[2]/li[{}]',
    'stars': '/div[3]/div/ul/li[{}]'
}

CLOSE_BUTTON_XPATH = '/html/body/div[4]/div[2]/div/div[1]/button'
BUTTON_XPATH_TEMPLATE = (
    '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/'
    'div[2]/div[2]/ul/li[{}]/div/div/div/div[1]/div[3]/button'
)

def load_country_codes(filepath='./data/raw/country_code.json'):
    """Load country codes from a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def initialize_driver():
    """Initialize the Chrome WebDriver with options."""
    options = configure_chrome_options()
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def configure_chrome_options():
    """Configure Chrome WebDriver options."""
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return options




def process_movie(driver, wait, country, country_code, rank):
    """Process a single movie entry."""
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
        log_error(country, rank, e)
    return content

def click_button(driver, wait, xpath:str):
    """
    Clicks a button specified by its XPATH.

    :param driver: WebDriver instance used to control the browser
    :param wait: WebDriverWait instance for setting timeout
    :param xpath: XPATH of the button to be clicked
    :return: None
    """
    button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    ActionChains(driver).click(button).perform()

def scrape_modal_content(wait, base_xpath:str, relative_xpaths:dict)->dict:
    """
    Extracts content from a modal dialog.

    :param wait: WebDriverWait instance for setting timeout
    :param base_xpath: Common XPATH shared by all elements
    :param relative_xpaths: Dictionary mapping element names to their relative XPATHs
    :return: Dictionary where keys are element names and values are their extracted content
    """
    extracted_content = {}
    for element_name, relative_xpath in relative_xpaths.items():
        try:
            full_xpath = base_xpath + relative_xpath
            if element_name == 'img':
                # Fetch 'src' attribute for images
                extracted_content[element_name] = wait.until(
                    EC.presence_of_element_located((By.XPATH, full_xpath))
                ).get_attribute('src')
            else:
                # Fetch text content for other elements
                extracted_content[element_name] = wait.until(
                    EC.presence_of_element_located((By.XPATH, full_xpath))
                ).text
        except Exception as e:
            print(f"Error fetching {element_name}: {e}")
    return extracted_content

def scrape_modal_data(driver, base_xpath:str, relative_xpaths:dict)->dict:
    """
    Extracts multiple values from a modal dialog using dynamic XPATHs.

    :param driver: WebDriver instance used to control the browser
    :param base_xpath: Base XPATH shared by all elements
    :param relative_xpaths: Dictionary where keys are element names and values are XPATH templates for each element
    :return: Dictionary where keys are element names and values are lists of extracted contents
    """
    extracted_data = {}

    for element_name, xpath_template in relative_xpaths.items():
        values = []
        index = 1
        while True:
            try:
                # Generate the full XPATH for the current element
                full_xpath = f"{base_xpath}{xpath_template.format(index)}"
                element = driver.find_element(By.XPATH, full_xpath)
                values.append(element.text)
                index += 1

            # Stop when no more elements are found
            except Exception:
                break
        extracted_data[element_name] = values
    
    return extracted_data

def log_error(country, rank, error):
    """Log an error with contextual information."""
    print(f"Error processing item {rank} for {country}: {error}")


def save_dict_as_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("JSON 파일이 성공적으로 저장되었습니다!")
    except Exception as e:
        print(f"An error occured:{e}")


def transform_content_to_result(content:dict[str,any], country:str) -> dict[str,any]: 
    """
    결과를 요구된 JSON 구조에 맞게 변환하는 함수입니다.
    
    :param content: 모달에서 추출한 콘텐츠 (dictionary)
    :param country: 영화가 속한 국가 (string)
    :return: 변환된 JSON 구조 (dictionary)
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


def crawling(top_n=10):
    """Main crawling function.
    자동으로 movies_data.json 중간저장
    """
    result = {"movies": []}
    country_code_dict = load_country_codes()
    today_date = str(datetime.today()).replace('-','')[:8]

    for country_code, country in tqdm(country_code_dict.items(), desc="Processing Countries"):
        with initialize_driver() as driver:
            wait = WebDriverWait(driver, 10)  # 타임아웃 설정
            country_url = BASE_URL.format(country_code)
            driver.get(country_url)

            for i in range(1, top_n + 1):
                content = process_movie(driver, wait, country, country_code, i)
                if content:
                    # transform_content_to_result 함수를 사용하여 결과 추가
                    result["movies"].append(transform_content_to_result(content, country))
        save_at = f'./data/raw/movies_data_{today_date}.json'
        save_dict_as_json(result, save_at)
    return result



