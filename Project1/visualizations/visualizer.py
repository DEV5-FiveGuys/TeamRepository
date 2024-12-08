import os
import re
import base64
from collections import Counter
from statistics import mean
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
from PIL import Image
from db_storage.utils import get_movies_by_country_name
from constant import *

class Visualizer():
    '''
        method:
            visualize_TOPK: 상위 K개의 영화를 HTML로 저장
            visualize_wordcloud: 영화 요약 텍스트 기반 워드클라우드 생성
            visualize_piechart: 장르 분포 파이차트 생성
            visualize_average_rating: 평균 별점 계산 및 시각화
    '''
    def __init__(self, country_name:str):
        self.country_name = country_name
        self.movies = get_movies_by_country_name(self.country_name)
        
    def visualize_TOPK(self, k: int = 5, filename: str = HTML_PATH+"TOP_K_movies.html") -> None:
        """
        TOP K개 영화 리스트 HTML 생성 및 저장
        """
        filtered_movies = [movie for movie in self.movies if 1 <= movie.get('rank', 0) <= k]
        movie_cards = ''.join([self.create_movie_card(movie) for movie in filtered_movies])
        self.save_movies_html(movie_cards, filename)
        
    def visualize_wordcloud(self, display_type: str='html', colormap: str="magma") -> None:
        """
        주어진 텍스트와 마스크 배열을 사용해 워드 클라우드 생성
        """
        mask_array = np.array(Image.open(MASK_PATH).convert(('L'))) if MASK_PATH else None
        stopwords = stopwords or set()
        # 국가별 데이터에서 summary 텍스트 추출
        text = " ".join(re.sub(r"[^\w\s]", "", movie["summary"]) for movie in self.movies) # 특수문자 제거
        wordcloud = WordCloud(
                        background_color="white",
                        mask=mask_array,
                        contour_color="black",  # 마스크 테두리 색상
                        contour_width=2,  # 마스크 테두리 두께
                        colormap=colormap,  # 색상 설정
                        max_words=100,  # 최대 표시 단어 수
                        prefer_horizontal= True, # 수평방향으로 글자 생성
                        stopwords=stopwords  # 불용어 설정
                    ).generate(text)
       
        if display_type == 'html':
            self.save_wordcloud_to_html(wordcloud)
        elif display_type == 'display':
            plt.figure(figsize=(12, 12))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.title('Word Cloud by Country', fontsize=18, weight="bold")
            plt.show()
            
    def visualize_piechart(self, top_n: int=8) -> None:
        plt.rcParams['font.family'] = 'Malgun Gothic' 
        plt.rcParams['axes.unicode_minus'] = False  # 음수 기호 깨짐 방지
        
        all_genres = [genre for movie in self.movies for genre in movie['genres']] # 모든 영화의 장르를 리스트로 수집
        genre_counts = Counter(all_genres) # 장르별로 카운트
        top_genres = dict(genre_counts.most_common(top_n)) # 상위 top_n개의 장르 추출
        self.save_pichart_to_html(top_genres=top_genres)
        
    def visualize_average_rating(self) -> None:
        average_rating = mean([float(movie['score']) for movie in self.movies]) # 전체 영화의 평균 별점 계산 (10점 만점)
        self.save_average_rating_to_html(average_rating=average_rating)
                
    def __display_svg_stars(self, rating: float) -> str:
        """
        별점을 SVG 형태로 생성 (10점 만점을 5점 만점으로 변환)
        """
        rating = rating / 2
        full_stars = int(rating)
        half_star = 1 if rating - full_stars >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        return full_star_svg * full_stars + half_star_svg * half_star + empty_star_svg * empty_stars
    
    def __create_movie_card(self, movie: dict) -> str:
        """
        영화 데이터를 카드 형식 HTML로 생성 (이미지, 제목, 연도, 별점)
        """
        stars_html = self.display_svg_stars(float(movie.get('score', 0)))
        return f"""
        <div style="display:inline-block; text-align:center; margin:10px; width:200px;">
            <img src="{movie.get('image', '')}" style="width:150px; height:200px; object-fit:cover; border:1px solid #ccc; border-radius:8px;">
            <div style="margin-top:10px; font-weight:bold;">{movie.get('title', 'Unknown')}</div>
            <div style="font-size:12px; color:gray;">{movie.get('release_year', 'N/A')}</div>
            <div style="margin-top:5px;">{stars_html}</div>
        </div>
        """

    def __save_movies_html(self, movie_cards: str) -> None:
        """
        영화 HTML 리스트를 저장
        """
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Top Movies</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .movie-container {{ display: flex; justify-content: center; flex-wrap: wrap; }}
            </style>
        </head>
        <body>
            <div class="movie-container">
                {movie_cards}
            </div>
        </body>
        </html>
        """
        # HTML 파일로 저장
        self.save_html(html_content, filepath=HTML_PATH+f'{self.country_name}/movies.html')
        
    def __save_wordcloud_to_html(self, wordcloud: WordCloud, title: str="Word Cloud") -> str:
        """
        워드 클라우드를 HTML로 저장합니다.
        """
        # 워드 클라우드를 이미지로 변환
        fig, ax = plt.subplots(figsize=(12, 12))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        plt.title(title, fontsize=18, weight="bold")
        
        # Base64 이미지 변환
        img_base64 = self.convert_to_base64(fig) 
        
        # HTML 코드 생성
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
        </head>
        <body>
            <div style="text-align: center;">
                <img src="data:image/png;base64,{img_base64}" alt="{title}">
            </div>
        </body>
        </html>
        """
        # HTML 파일로 저장
        self.save_html(html_content, filepath=HTML_PATH+f'{self.country_name}/wordcloud.html')
        
    def __save_pichart_to_html(self, top_genres: dict):    
       # 파이 차트 생성
        labels = list(top_genres.keys())
        sizes = list(top_genres.values())
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))  # 색상 설정
        fig, ax = plt.subplots(figsize=(12, 10))
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,  # 가장 큰 비율 항목을 맨 위로
            colors=colors,
            textprops={'fontsize': 20, 'weight': 'bold'},
            wedgeprops={'edgecolor': 'white', 'linewidth': 4}  # 경계선 추가
        )
        ax.set_title("인기 장르", fontsize=18, weight="bold")  
        plt.setp(autotexts, size=12, weight="bold")
        # 현재 Figure를 Base64 이미지로 변환
        img_base64 = self.convert_to_base64(fig)

        # HTML 생성
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>영화 장르 분석</title>
        </head>
        <body>
            <img src="data:image/png;base64,{img_base64}" alt="Pie Chart" style="display: block; margin: 0 auto; max-width: 100%;">
        </body>
        </html>
        """
        # HTML 파일 저장
        self.save_html(html_content, filepath=HTML_PATH+f'{self.country_name}/pie.html')
        
    def __save_average_rating_to_html(self, average_rating: float):
        svg_stars = self.display_svg_stars(average_rating)
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Average Movie Rating</title>
        </head>
        <body>
            <h1 style="text-align: center;">Average Rating: {average_rating:.1f}/10</h1>
            <div style="text-align: center;">{svg_stars}</div>
        </body>
        </html>
        """
        self.save_html(html_content, filepath=HTML_PATH+f'{self.country_name}/average_rating.html')
        
    def __save_html(self, content: str, filepath: str) -> None:
        """
        HTML 파일 저장
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"HTML 파일이 '{filepath}'에 저장되었습니다.")
        
    def __convert_to_base64(fig=None, format="png", dpi=300, bbox_inches="tight") -> str:
        """
        Matplotlib Figure를 Base64로 변환
        
        Args:
            fig (matplotlib.figure.Figure, optional): 변환할 Matplotlib Figure 객체 (None이면 현재 활성 Figure 사용).
            format (str): 저장할 이미지 형식 (기본값: "png").
            dpi (int): 이미지 해상도 (기본값: 300).
            bbox_inches (str): 저장할 이미지의 여백 설정 (기본값: "tight").
            
        Returns:
            str: Base64로 인코딩된 이미지 문자열.
        """
        if fig is None:
            fig = plt.gcf()  # 현재 활성 Figure 가져오기

        # 이미지 데이터를 메모리에 저장
        buffer = BytesIO()
        fig.savefig(buffer, format=format, dpi=dpi, bbox_inches=bbox_inches)
        buffer.seek(0)  # 버퍼의 시작으로 이동

        # Base64로 인코딩
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close(fig)
        buffer.close()

        return image_base64
    