import os
import json
import pytest
from unittest.mock import MagicMock, patch
from .utils import MovieCrawler

@pytest.fixture
def mock_wait():
    """
    WebDriverWait 모의 객체를 생성하는 픽스처.
    """
    mock_wait = MagicMock()
    mock_wait.until.return_value = MagicMock()
    return mock_wait

@pytest.fixture
def mock_driver():
    """
    WebDriver 모의 객체를 생성하는 픽스처.
    """
    return MagicMock()

@pytest.fixture
def mock_crawler():
    """
    MovieCrawler 인스턴스를 생성하는 픽스처.
    """
    return MovieCrawler(top_n=1)

def test_load_country_codes():
    """
    load_country_codes 함수가 올바르게 JSON 파일을 로드하는지 테스트합니다.
    """
    crawler = MovieCrawler()
    with patch("builtins.open", new_callable=MagicMock) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(
            {"KR": "South Korea", "US": "United States"}
        )
        country_codes = crawler.load_country_codes()
        assert country_codes == {"KR": "South Korea", "US": "United States"}

def test_initialize_driver(mock_crawler):
    """
    initialize_driver 함수가 WebDriver 객체를 초기화하는지 테스트합니다.
    """
    with patch("crawler.webdriver.Chrome") as mock_chrome:
        driver = mock_crawler.initialize_driver()
        assert driver == mock_chrome.return_value

def test_process_movie(mock_driver, mock_wait, mock_crawler):
    """
    process_movie 함수가 올바르게 작동하는지 테스트합니다.
    """
    mock_crawler.process_movie(mock_driver, mock_wait, "South Korea", "KR", 1)
    mock_wait.until.assert_called()

def test_crawling(mock_crawler):
    """
    crawling 함수가 올바르게 동작하는지 테스트합니다.
    """
    with patch("os.path.abspath") as mock_abspath, patch("crawler.MovieCrawler.save_dict_as_json"):
        mock_abspath.return_value = "/absolute/path/to/file.json"
        response = mock_crawler.crawling()
        
        # 성공 여부와 파일 저장 경로 확인
        assert response["success"] is True
        assert response["file_path"] == "/absolute/path/to/file.json"
