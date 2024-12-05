from selenium.webdriver.support.ui import WebDriverWait
import time
import json 
from utils import *
from tqdm import tqdm



def main(top_n=10):
    """Main crawling function."""
    result = {"movies": []}
    country_code_dict = load_country_codes()

    for country_code, country in tqdm(country_code_dict.items(), desc="Processing Countries"):
        with initialize_driver() as driver:
            wait = WebDriverWait(driver, 10)  # 타임아웃 설정
            country_url = BASE_URL.format(country_code)
            driver.get(country_url)
            time.sleep(2)  # 페이지 로드 대기

            for i in range(1, top_n + 1):
                content = process_movie(driver, wait, country, country_code, i)
                if content:
                    # 결과 추가 (요구된 JSON 구조에 맞게 변환)
                    result["movies"].append({
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
                    })
    return result


if __name__ == "__main__":
    try:
        result = main(top_n = 10)
        with open('C:/Users/chauj/Desktop/develop/TeamRepository/WebCrawling/data/raw/movies_data_3.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print("JSON 파일이 성공적으로 저장되었습니다!")
    except Exception as e:
        print(f"An error occured:{e}")