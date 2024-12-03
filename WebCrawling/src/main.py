from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json 
from utils import *


def main(top_n=10): # top_n <= 50까지만 문제없이 작동함
    """메인 함수."""
    result = []
    url = 'https://www.imdb.com/search/title/?countries={}'
    base_xpath = '/html/body/div[4]/div[2]/div/div[2]/div/div'
    relative_xpaths = {
        'img': '/div[1]/div[1]/div/div/img',
        'title': '/div[1]/div[2]/div[1]/a/h3',
        'year': '/div[1]/div[2]/ul[1]/li[1]',
        'score': '/div[1]/div[2]/div[2]/span/span[1]',
        'summary': '/div[2]'
    }
    

    elements_path ={'genre': '/div[1]/div[2]/ul[2]/li[{}]','stars': '/div[3]/div/ul/li[{}]'}
    # country_code.json 불러오기
        
    # JSON 파일 읽어서 딕셔너리로 변환
    with open('./data/raw/country_code.json', 'r', encoding='utf-8') as file:
        country_code_dict = json.load(file)

    for country_code, country in country_code_dict.items():
        # result.extend(main(country_code=country, top_n=1))
        # 루프가 돌아가는 시간 책정
        start_time = time.time()
        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
            driver.get(url.format(country_code))
            wait = WebDriverWait(driver, 10)  # WebDriverWait의 타임아웃 시간을 조절


            for i in range(1, top_n + 1):
                print(f"Processing item {i}...")
                try:
                    # 버튼 클릭
                    button_xpath = f'//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li[{i}]/div/div/div/div[1]/div[3]/button'
                    click_button(driver, wait, button_xpath)
                    time.sleep(0.5)

                    # 콘텐츠 크롤링
                    content = scrape_modal_content(wait, base_xpath, relative_xpaths)
                    
                    time.sleep(2)

                    # content_dict에 국가명 추가
                    content['country'] = country
                    print(country)
                    # content_dict에 장르, 배우 등 list요소 추가 
                    content2 = scrape_modal_data(driver, base_xpath, elements_path)

                    # content와 content2 합치기
                    content = content|content2

                    # content_dict에 순위 추가
                    content['rank'] = i

                    result.append(content)

                    # 모달 닫기
                    close_button_xpath = '/html/body/div[4]/div[2]/div/div[1]/button'
                    click_button(driver, wait, close_button_xpath)
                    time.sleep(0.5)

                except Exception as e:
                    print(f"Error processing item {i}: {e}")

        # 루프가 끝나는 시간 기록
        end_time = time.time()
        print(end_time - start_time)                
    return result


if __name__ == "__main__":
    # result = []

    # # country_code.json 불러오기
        
    # # JSON 파일 경로
    # file_path = './data/raw/country_code.json'

    # # JSON 파일 읽어서 딕셔너리로 변환
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     country_code_dict = json.load(file)

    # countries = list(country_code_dict.keys())

    # for country in countries:
        # result.extend(main(country_code=country, top_n=1))
        # 국가 코드를 국가명으로 변경
        # result[country] = country_code_dict[country]

    # print(result)
    
    # JSON 파일로 저장
    
    result = main(top_n = 1)
    with open('./data/raw/movies_data_2.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    print("JSON 파일이 성공적으로 저장되었습니다!")
    