from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import re
from io import BytesIO
import base64

# 1. 이미지 파일을 마스크로 변환
def load_mask_image(mask_path):
    """
    이미지 파일을 로드하고 마스크 배열로 변환합니다.
    """
    mask_image = Image.open(mask_path).convert("L")  # 흑백 이미지로 변환
    return np.array(mask_image)

# 2. 국가별 summary 텍스트 합치기
def combine_text_by_country(movies, selected_country):
    """
    특정 국가의 summary 텍스트를 합칩니다.
    """
    return " ".join(
        [
            re.sub(r"[^\w\s]", "", movie["summary"])  # 특수문자 제거
            for movie in movies
            if movie["country"] == selected_country
        ]
    )

# 3. 워드 클라우드 생성
def generate_wordcloud(text, mask_array, stopwords, colormap="Oranges"):
    """
    주어진 텍스트와 마스크 배열을 사용해 워드 클라우드를 생성합니다.
    """
    return WordCloud(
        background_color="white",
        mask=mask_array,
        contour_color="black",  # 마스크 테두리 색상
        contour_width=10,  # 마스크 테두리 두께
        colormap=colormap,  # 색상 설정
        max_words=200,  # 최대 표시 단어 수
        stopwords=stopwords  # 불용어 설정
    ).generate(text)

# 4. 워드 클라우드 표시
def display_wordcloud(wordcloud, title="Word Cloud"):
    """
    워드 클라우드를 화면에 표시합니다.
    """
    plt.figure(figsize=(12, 12))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title, fontsize=18, weight="bold")
    plt.show()

# 5. 워드 클라우드를 HTML로 저장
def save_wordcloud_to_html(wordcloud, html_filename="wordcloud.html", title="Word Cloud"):
    """
    워드 클라우드를 HTML로 저장합니다.
    """
    # 워드 클라우드를 이미지로 변환
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    plt.title(title, fontsize=18, weight="bold")
    
    # 이미지를 BytesIO로 저장
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png", bbox_inches='tight')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
    img_buffer.close()
    
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
    with open(html_filename, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)
    
    print(f"HTML 파일이 {html_filename}로 저장되었습니다.")


# 테스트 데이터
movies = [
    {
    "img": "https://m.media-amazon.com/images/M/MV5BYTYzMTlmNDctNmVkNS00YzRlLWE5MjAtODdjZWRkYzRlNWVlXkEyXkFqcGc@._V1_QL75_UX72_CR0,0,72,107_.jpg",
    "title": "오징어 게임",
    "year": "2021–2025",
    "score": "8.0",
    "summary": "Hundreds of cash-strapped players accept a strange invitation to compete in children's games. Inside, a tempting prize awaits with deadly high stakes: a survival game that has a whopping 45.6 billion-won prize at stake.",
    "country": "KR",
    "genre": ["Action", "Drama", "Mystery"],
    "stars": ["Lee Jung-jae", "Park Hae-soo", "Nandito Hidayattullah Putra"],
    "rank": 1
},
    {
    "img": "https://m.media-amazon.com/images/M/MV5BZWMyMjRkYzMtZDMyNS00ZTEwLTg3ZmMtYTljZDMxMjg2MjNhXkEyXkFqcGc@._V1_QL75_UY207_CR3,0,140,207_.jpg",
    "title": "지금 거신 전화는",
    "year": "2024-",
    "score": "8.4",
    "summary": "Baek Sa Eon, a former presidential spokesman, marries Hong Hui Ju, a mute newspaper heiress, in an arranged union. When Hui Ju is kidnapped, their distant relationship is challenged as they navigate the crisis.",
    "country": "KR",
    "genre": ["Drama", "Mystery", "Romance", "Thriller"],
    "stars": ["Yoo Yeon-seok", "Chae Soo-bin", "Heo Nam-jun"],
    "rank": 2
},
    {
    "img": "https://m.media-amazon.com/images/M/MV5BYjk1Y2U4MjQtY2ZiNS00OWQyLWI3MmYtZWUwNmRjYWRiNWNhXkEyXkFqcGc@._V1_QL75_UX140_CR0,0,140,207_.jpg",
    "title": "기생충",
    "year": "2019",
    "score": "8.5",
    "summary": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
    "country": "KR",
    "genre": ["Dark Comedy", "Korean Drama", "Psychological Thriller", "Tragedy", "Drama"],
    "stars": ["Song Kang-ho", "Cho Yeo-jeong","Lee Sun-kyun", "Choi Woo-sik"],
    "rank": 3
},
            {
    "img": "https://m.media-amazon.com/images/M/MV5BMTI3NTQyMzU5M15BMl5BanBnXkFtZTcwMTM2MjgyMQ@@._V1_QL75_UX140_CR0,0,140,207_.jpg",
    "title": "올드보이",
    "year": "2003",
    "score": "8.3",
    "summary": "After being kidnapped and imprisoned for fifteen years, Oh Dae-Su is released, only to find that he must track down his captor in five days.",
    "country": "KR",
    "genre": ["Dark Comedy", "One-Person Army Action", "Psychological Thriller", "Action", "Drama"],
    "stars": ["Choi Min-sik", "Yoo Ji-tae", "Kang Hye-jeong"],
    "rank": 4
},
                {
    "img": "https://m.media-amazon.com/images/M/MV5BNjgwYmJhYjgtYzJhYi00NmU5LWE1ZjEtOWRjOWJkN2M3MTU2XkEyXkFqcGc@._V1_QL75_UY207_CR3,0,140,207_.jpg",
    "title": "강남 비사이드",
    "year": "2024-",
    "score": "7.3",
    "summary": "In Gangnam, Seoul, Jae-Hee knows a secret about a series of disappearances but then vanishes herself. Detective Kang, outlaw Yoon, and Prosecutor Min pursue the truth for their own reasons.",
    "country": "KR",
    "genre": ["Action", "Crime", "Drama", "Mystery", "Thriller"],
    "stars": ["Jo Woo-jin", "Ji Chang-wook", "Ha Yoon-kyung"],
    "rank": 5
}
]

# 마스크 로드
mask_path = "C:\\Users\\ydy92\\Desktop\\IMDb_Visualization\\film_camera_mask.png" # 경로 수정해야돼요!
mask_array = load_mask_image(mask_path)

# 국가별 텍스트 합치기
selected_country = "KR"
text = combine_text_by_country(movies, selected_country)

# 불용어 설정
stopwords = {"a", "the", "and", "of", "to", "is", "with", "in", "on", "at", "for", "this", "that", "their", "hui", "ju"} # 이건 데이터 여러개 받아보고 수정하겠습니다.

# 워드 클라우드 생성
wordcloud = generate_wordcloud(text, mask_array, stopwords)

# 워드 클라우드 표시
# display_wordcloud(wordcloud, title=f"Word Cloud by Country ({selected_country})")

# HTML 파일로 저장
save_wordcloud_to_html(wordcloud, html_filename="wordcloud.html", title=f"Word Cloud by Country ({selected_country})")