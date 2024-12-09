import re
import os
import sys
import django
import base64
from collections import Counter
from statistics import mean
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from wordcloud import WordCloud
from PIL import Image


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project1.settings')

# 이후 Django를 초기화

django.setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project1.settings')

django.setup()

# Django 앱에서 데이터베이스 접근
from db_storage.utils import *
from visualizations.constant import *

class Visualizer():
    matplotlib.use('Agg')

    def __init__(self, country_name: str):
        self.country_name = country_name
        self.movies = get_movies_by_country_name(self.country_name)

    def display_svg_stars(self, rating: float) -> str:
        """
        별점을 SVG 형태로 생성 (10점 만점을 5점 만점으로 변환)
        """
        rating = rating / 2
        full_stars = int(rating)
        half_star = 1 if rating - full_stars >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        return full_star_svg * full_stars + half_star_svg * half_star + empty_star_svg * empty_stars
    
    def create_movie_card(self, movie: dict) -> str:
        """
        영화 데이터를 카드 형식 HTML로 생성 (이미지, 제목, 연도, 별점)
        """
        stars_html = self.display_svg_stars(float(movie.get('score', 0)))
        return f"""
        <div class="movie-card">
            <img src="{movie.get('image', '')}" alt="Movie Image">
            <div>{movie.get('title', 'Unknown')}</div>
            <div style="font-size:12px; color:gray;">{movie.get('release_year', 'N/A')}</div>
            <div>{stars_html}</div>
        </div>
        """

    # def convert_to_base64(self, fig=None) -> str:
    #     """
    #     Matplotlib Figure를 Base64로 변환
    #     """
    #     if fig is None:
    #         fig = plt.gcf()
    #     buffer = BytesIO()
    #     plt.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
    #     buffer.seek(0)
    #     image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    #     plt.close(fig)
    #     buffer.close()
    #     return image_base64

    def convert_to_base64(self, img=None) -> str:
        """
        Convert a PIL Image to Base64 string.
        """
        if img is None:
            img = plt.gcf()  # If no image is provided, get the current figure

        # If the input is a PIL image, save it to a BytesIO buffer
        if isinstance(img, Image.Image):
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            return image_base64

        # If the input is a matplotlib figure, save it as PNG
        elif isinstance(img, plt.Figure):
            buffer = BytesIO()
            img.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            return image_base64

        # In case the input is neither a PIL image nor a matplotlib figure
        raise TypeError("Input must be a PIL Image or a matplotlib Figure")



    def generate_piechart(self, top_k: int = 8) -> str:
        """
        파이차트 생성 및 Base64 변환
        """
        all_genres = [genre for movie in self.movies for genre in movie['genres']]
        genre_counts = Counter(all_genres)
        top_genres = dict(genre_counts.most_common(top_k))
        labels = list(top_genres.keys())
        sizes = list(top_genres.values())
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))

        # Create the figure and plot the pie chart
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            textprops={'fontsize': 12},
            wedgeprops={'edgecolor': 'white', 'linewidth': 1}
        )
        ax.set_title("장르별 분포", fontsize=14, weight="bold")

        # Pass the figure to convert_to_base64 and ensure it's a valid object
        try:
            return self.convert_to_base64(fig)
        except TypeError as e:
            print("Error in converting to base64:", e)
            return ''


    def generate_wordcloud(self, colormap: str = "magma") -> str:
        """
        워드클라우드 생성 및 Base64 변환
        """
        text = " ".join(re.sub(r"[^\w\s]", "", movie["summary"]) for movie in self.movies)
        mask_array = np.array(Image.open(MASK_PATH).convert(('L'))) if MASK_PATH else None
        stopwords = STOPWORDS or set()
        wordcloud = WordCloud(
            background_color="white",
            mask=mask_array,
            contour_color="black",
            contour_width=2,
            colormap=colormap,
            max_words=100,
            prefer_horizontal=True,
            stopwords=stopwords
        ).generate(text)
        return self.convert_to_base64(wordcloud.to_image())

    # def generate_piechart(self, top_k: int = 8) -> str:
    #     """
    #     파이차트 생성 및 Base64 변환
    #     """
    #     all_genres = [genre for movie in self.movies for genre in movie['genres']]
    #     genre_counts = Counter(all_genres)
    #     top_genres = dict(genre_counts.most_common(top_k))
    #     labels = list(top_genres.keys())
    #     sizes = list(top_genres.values())
    #     colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
    #     fig, ax = plt.subplots(figsize=(6, 6))
    #     ax.pie(
    #         sizes,
    #         labels=labels,
    #         autopct='%1.1f%%',
    #         startangle=90,
    #         colors=colors,
    #         textprops={'fontsize': 12},
    #         wedgeprops={'edgecolor': 'white', 'linewidth': 1}
    #     )
    #     ax.set_title("장르별 분포", fontsize=14, weight="bold")
    #     return self.convert_to_base64(fig)
    def generate_piechart(self, top_k: int = 8) -> str:
        """
        파이차트 생성 및 Base64 변환
        """
        all_genres = [genre for movie in self.movies for genre in movie['genres']]
        genre_counts = Counter(all_genres)
        top_genres = dict(genre_counts.most_common(top_k))
        labels = list(top_genres.keys())
        sizes = list(top_genres.values())
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))

        # Create the figure and plot the pie chart
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            textprops={'fontsize': 12},
            wedgeprops={'edgecolor': 'white', 'linewidth': 1}
        )
        ax.set_title("장르별 분포", fontsize=14, weight="bold")

        # Pass the figure to convert_to_base64 and ensure it's a valid object
        try:
            return self.convert_to_base64(fig)
        except TypeError as e:
            print("Error in converting to base64:", e)
            return ''


    def visualize_all(self, top_k: int = 5, piechart_k: int = 8, colormap: str = "magma") -> None:
        """
        모든 시각화를 통합하여 하나의 HTML로 저장 (중복 제거)
        """
        # 영화 카드 생성
        filtered_movies = [movie for movie in self.movies if 1 <= movie.get('rank', 0) <= top_k]
        movie_cards = ''.join([self.create_movie_card(movie) for movie in filtered_movies])

        # 워드클라우드와 파이차트 생성
        wordcloud_base64 = self.generate_wordcloud(colormap=colormap)
        piechart_base64 = self.generate_piechart(top_k=piechart_k)

        # 평균 별점 계산 및 SVG 생성
        average_rating = mean([float(movie['score']) for movie in self.movies])
        stars_html = self.display_svg_stars(average_rating)

        # HTML 생성
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Movie Visualizations</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .movie-container {{
                    display: flex;
                    justify-content: center;
                    flex-wrap: wrap;
                    gap: 10px;
                    margin-bottom: 40px;
                }}
                .movie-card {{
                    text-align: center;
                    width: 150px;
                }}
                .movie-card img {{
                    width: 100%;
                    height: auto;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                }}
                .visualizations {{
                    display: flex;
                    justify-content: space-around;
                    align-items: center;
                    flex-wrap: wrap;
                }}
                .visualization-item {{
                    text-align: center;
                    margin: 20px;
                }}
                .visualization-item img {{
                    max-width: 250px;
                    height: auto;
                }}
            </style>
        </head>
        <body>
            <div class="movie-container">
                {movie_cards}
            </div>
            <div class="visualizations">
                <div class="visualization-item">
                    <h3>장르별 분포</h3>
                    <img src="data:image/png;base64,{piechart_base64}" alt="Pie Chart">
                </div>
                <div class="visualization-item">
                    <h3>태그 Word Cloud</h3>
                    <img src="data:image/png;base64,{wordcloud_base64}" alt="Word Cloud">
                </div>
                <div class="visualization-item">
                    <h3>평균 별점</h3>
                    <div>{stars_html}</div>
                </div>
            </div>
        </body>
        </html>
        """

        # HTML 저장
        filepath = HTML_PATH + f'{self.country_name}/combined.html'
        self.save_html(html_content, filepath)

    def save_html(self, content: str, filepath: str) -> None:
        """
        HTML 파일 저장
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"HTML 파일이 '{filepath}'에 저장되었습니다.")


visualizer = Visualizer("Brazil")  # 예: 'Korea'라는 나라의 영화 데이터를 가져옴
visualizer.visualize_all(top_k=5, piechart_k=8, colormap="viridis")
