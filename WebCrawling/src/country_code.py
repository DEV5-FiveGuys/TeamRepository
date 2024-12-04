from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json 
from utils import *

url = 'https://www.imdb.com/search/title/'
base_xpath = '//*[@id="react-autowhatever-1--item-'
relative_xpaths = {'country':'{}"]/div/div/label',
                    'country_code':'{}"]/div/div/text'}
label_xpath = '//*[@id="react-autowhatever-1--item-{}"]/div/div/label'


with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    driver.get(url)
    wait = WebDriverWait(driver, 20)  # WebDriverWait의 타임아웃 시간을 늘림

    button_xpath = '//*[@id="countryAccordion"]/div[1]/label/span[1]/div'
    click_button(driver, wait, button_xpath)
    time.sleep(0.5)

    button_xpath2 = '//*[@id="accordion-item-countryAccordion"]/div/div/div[1]/div[1]/input'
    click_button(driver, wait, button_xpath2)
    time.sleep(0.5)

    country_dict = {}
    index = 0

    while True:
        try:
            # label속성 데이터 추출하기
            label_element = driver.find_element(By.XPATH, label_xpath.format(index))
            checkbox_id = label_element.get_attribute('for')
            country = label_element.text
            country_dict[checkbox_id.split('-')[-1]]=country
            
            index += 1

        except Exception:
            break

    
    print(country_dict)
    
with open('country_code.json', 'w', encoding='utf-8') as f:
    json.dump(country_dict, f, ensure_ascii=False, indent=4)
    
print("JSON 파일이 성공적으로 저장되었습니다!")
