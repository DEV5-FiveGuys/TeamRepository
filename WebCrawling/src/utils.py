from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json 
from utils import *
from tqdm import tqdm




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



def configure_chrome_options():
    """Chrome 옵션 설정."""
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    # options.add_argument("--headless")  # 브라우저를 화면에 표시하지 않음
    return options

def crawling(top_n=10): # top_n <= 50까지만 문제없이 작동함
    """메인 함수."""
    result = []
    base_url  = 'https://www.imdb.com/search/title/?countries={}'
    base_xpath = '/html/body/div[4]/div[2]/div/div[2]/div/div'
    relative_xpaths = {
        'img': '/div[1]/div[1]/div/div/img',
        'title': '/div[1]/div[2]/div[1]/a/h3',
        'year': '/div[1]/div[2]/ul[1]/li[1]',
        'score': '/div[1]/div[2]/div[2]/span/span[1]',
        'summary': '/div[2]'
    }
    

    elements_path ={'genre': '/div[1]/div[2]/ul[2]/li[{}]','stars': '/div[3]/div/ul/li[{}]'}
    
    # country_code.json 파일 읽어서 딕셔너리로 변환
    with open('./data/raw/temp_country_code.json', 'r', encoding='utf-8') as file:
        country_code_dict = json.load(file)

    options = configure_chrome_options()

    for country_code, country in tqdm(country_code_dict.items(), desc="Processing Countries"):
        # result.extend(main(country_code=country, top_n=1))
        # 루프가 돌아가는 시간 책정
        start_time = time.time()
        with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options =  options) as driver:
            wait = WebDriverWait(driver, 10)  # 타임아웃 설정

            # URL 생성 및 페이지 로드
            country_url = base_url.format(country_code)
            driver.get(country_url)
            time.sleep(2)  # 페이지 로드 대기


            for i in range(1, top_n + 1):
                try:
                    print(f"Processing item {i} for {country}({country_code})")
                    button_xpath = f'//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li[{i}]/div/div/div/div[1]/div[3]/button'
                    
                    # 버튼 클릭
                    click_button(driver, wait, button_xpath)
                    time.sleep(0.5)

                    # 콘텐츠 크롤링
                    content = scrape_modal_content(wait, base_xpath, relative_xpaths)

                    # content_dict에 국가명 추가
                    content['country'] = country

                    # content_dict에 장르, 배우 등 list요소 추가 
                    content.update(scrape_modal_data(driver, base_xpath, elements_path))

                    # content_dict에 순위 추가
                    content['rank'] = i

                    result.append(content)

                    # 모달 닫기
                    close_button_xpath = '/html/body/div[4]/div[2]/div/div[1]/button'
                    click_button(driver, wait, close_button_xpath)
                    time.sleep(0.5)

                except Exception as e:
                    print(f"Error processing item {i} for {country}: {e}")

        # 루프가 끝나는 시간 기록
        elapsed_time = time.time() - start_time
        print(f"Finished processing {country} in {elapsed_time:.2f} seconds.")            
    return result