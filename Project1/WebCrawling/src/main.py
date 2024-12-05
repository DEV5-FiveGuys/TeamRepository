from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import json 
from utils import *
from tqdm import tqdm
from datetime import datetime


def main(top_n=10):
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
        save_at = f'C:/Users/chauj/Desktop/develop/TeamRepository/Project1/WebCrawling/data/raw/movies_data_{today_date}.json'
        save_dict_as_json(result, save_at)
    return result


if __name__ == "__main__":
    main()