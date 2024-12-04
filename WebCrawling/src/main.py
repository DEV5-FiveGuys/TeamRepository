from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json 
from utils import *


def main(country_code='KR', top_n=10): # top_n <= 50까지만 문제없이 작동함
    """메인 함수."""
    result = []
    url = f'https://www.imdb.com/search/title/?countries={country_code}'
    common_path = '/html/body/div[4]/div[2]/div/div[2]/div/div'
    relative_loc = {
        'img': '/div[1]/div[1]/div/div/img',
        'title': '/div[1]/div[2]/div[1]/a/h3',
        'year': '/div[1]/div[2]/ul[1]/li[1]',
        'score': '/div[1]/div[2]/div[2]/span/span[1]',
        'summary': '/div[2]'
    }
    

    elements_path ={'genre': '/div[1]/div[2]/ul[2]/li[{}]','stars': '/div[3]/div/ul/li[{}]'}
    
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        driver.get(url)
        wait = WebDriverWait(driver, 20)  # WebDriverWait의 타임아웃 시간을 늘림


        for i in range(1, top_n + 1):
            print(f"Processing item {i}...")
            try:
                # 버튼 클릭
                button_xpath = f'//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li[{i}]/div/div/div/div[1]/div[3]/button'
                click_button(driver, wait, button_xpath)
                time.sleep(0.5)

                # 콘텐츠 크롤링
                content = scrape_content(wait, common_path, relative_loc)
                
                time.sleep(2)

                # content_dict에 국가코드 추가
                content['country'] = country_code

                # content_dict에 장르, 배우 등 list요소 추가 
                content = extract_elements(driver, content, common_path, elements_path)

                # content_dict에 순위 추가
                content['rank'] = i

                result.append(content)

                # 모달 닫기
                close_button_xpath = '/html/body/div[4]/div[2]/div/div[1]/button'
                click_button(driver, wait, close_button_xpath)
                time.sleep(0.5)

            except Exception as e:
                print(f"Error processing item {i}: {e}")
                
    return result


if __name__ == "__main__":
    result = []
    countries = ["KR","KP"]

    for country in countries:
        result.extend(main(country_code=country, top_n=10))
    
    # JSON 파일로 저장
    
    with open('movies_data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    print("JSON 파일이 성공적으로 저장되었습니다!")
    