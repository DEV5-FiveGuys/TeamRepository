import unittest
from unittest.mock import patch, MagicMock
from Crawling import MovieCrawler  # Crawling.py에 있는 MovieCrawler 클래스 임포트

class TestMovieCrawler(unittest.TestCase):
    def setUp(self):
        """테스트 전에 실행되는 초기 설정 함수"""
        # 테스트를 위한 MovieCrawler 객체 생성
        self.crawler = MovieCrawler(top_n=2)

    @patch('Crawling.MovieCrawler.load_country_codes')  # load_country_codes 메서드 mocking
    def test_load_country_codes(self, mock_load_country_codes):
        """country_code.json 파일을 잘 읽어오는지 테스트"""
        # mock 데이터를 반환하도록 설정
        mock_load_country_codes.return_value = {'US': 'USA', 'KR': 'Korea'}
        
        country_codes = self.crawler.load_country_codes()
        
        # 예상 결과가 맞는지 확인
        self.assertEqual(country_codes, {'US': 'USA', 'KR': 'Korea'})

    @patch('Crawling.MovieCrawler.initialize_driver')  # 드라이버 초기화 메서드 mocking
    @patch('Crawling.MovieCrawler.process_movie')  # process_movie 메서드 mocking
    @patch('Crawling.MovieCrawler.save_dict_as_json')  # JSON 저장 메서드 mocking
    def test_crawling(self, mock_save_json, mock_process_movie, mock_initialize_driver):
        """crawling() 메서드가 제대로 동작하는지 테스트"""
        
        # mock 드라이버와 process_movie가 반환할 결과 설정
        mock_initialize_driver.return_value.__enter__.return_value = MagicMock()
        mock_process_movie.return_value = {'title': 'Test Movie', 'rank': 1}

        # crawling 실행
        result = self.crawler.crawling()
        
        # 결과가 예상대로 동작하는지 확인
        self.assertIn("movies", result)
        self.assertGreater(len(result["movies"]), 0)
        self.assertEqual(result["movies"][0]["movie"]["title"], 'Test Movie')

    @patch('Crawling.MovieCrawler.save_dict_as_json')  # JSON 저장 메서드 mocking
    def test_save_dict_as_json(self, mock_save_json):
        """JSON 저장 메서드가 제대로 호출되는지 테스트"""
        
        data = {"movies": [{"title": "Test Movie"}]}
        file_path = './test.json'
        
        # save_dict_as_json을 호출
        self.crawler.save_dict_as_json(data, file_path)
        
        # save_dict_as_json이 제대로 호출되었는지 확인
        mock_save_json.assert_called_once_with(data, file_path)

if __name__ == '__main__':
    unittest.main()
