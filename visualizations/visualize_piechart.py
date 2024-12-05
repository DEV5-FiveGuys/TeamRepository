from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# html 렌더링
import io
import base64

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic' 
plt.rcParams['axes.unicode_minus'] = False  # 음수 기호 깨짐 방지

# JSON 데이터에서 상위 n개의 장르를 카운트하여 반환
def count_top_genres(movies, top_n=8):
    """
    JSON 데이터에서 상위 n개의 장르를 카운트하여 반환합니다.

    Parameters:
        movies (list): 영화 데이터 리스트(JSON 형식)
        top_n (int): 상위 몇 개의 장르를 반환할지 설정

    Returns:
        dict: 상위 n개의 장르와 그 개수
    """
    # 모든 영화의 장르를 평탄화(flatten)하여 리스트로 수집
    all_genres = [genre for movie in movies for genre in movie['genres']]
    
    # 장르별로 카운트
    genre_counts = Counter(all_genres)
    
    # 상위 top_n개의 장르 추출
    top_genres = genre_counts.most_common(top_n)
    
    # 딕셔너리 형태로 변환하여 반환
    return dict(top_genres)


# 예시 데이터
movies = [
    {
    "rank": 1,
    "title": "오징어 게임",
    "release_year": "2021–2025",
    "score": 8.0,
    "summary": "Hundreds of cash-strapped players accept a strange invitation to compete in children's games. Inside, a tempting prize awaits with deadly high stakes: a survival game that has a whopping 45.6 billion-won prize at stake.",
    "image": "https://m.media-amazon.com/images/M/MV5BYTYzMTlmNDctNmVkNS00YzRlLWE5MjAtODdjZWRkYzRlNWVlXkEyXkFqcGc@._V1_QL75_UX72_CR0,0,72,107_.jpg",
    "genres": ["Action", "Drama", "Mystery"],
    "actors": ["Lee Jung-jae", "Park Hae-soo", "Nandito Hidayattullah Putra"]
},
{
    "rank": 2,
    "title": "지금 거신 전화는",
    "release_year": "2024-",
    "score": 8.4,
    "summary": "Baek Sa Eon, a former presidential spokesman, marries Hong Hui Ju, a mute newspaper heiress, in an arranged union. When Hui Ju is kidnapped, their distant relationship is challenged as they navigate the crisis.",
    "image": "https://m.media-amazon.com/images/M/MV5BZWMyMjRkYzMtZDMyNS00ZTEwLTg3ZmMtYTljZDMxMjg2MjNhXkEyXkFqcGc@._V1_QL75_UY207_CR3,0,140,207_.jpg",
    "genres": ["Drama", "Mystery", "Romance", "Thriller"],
    "actors": ["Yoo Yeon-seok", "Chae Soo-bin", "Heo Nam-jun"]
},
{
    "rank": 3,
    "title": "기생충",
    "release_year": "2019",
    "score": 8.5,
    "summary": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
    "image": "https://m.media-amazon.com/images/M/MV5BYjk1Y2U4MjQtY2ZiNS00OWQyLWI3MmYtZWUwNmRjYWRiNWNhXkEyXkFqcGc@._V1_QL75_UX140_CR0,0,140,207_.jpg",
    "genres": ["Dark Comedy", "Korean Drama", "Psychological Thriller", "Tragedy", "Drama"],
    "actors": ["Song Kang-ho", "Cho Yeo-jeong", "Lee Sun-kyun", "Choi Woo-sik"]
},
{
    "rank": 4,
    "title": "올드보이",
    "release_year": "2003",
    "score": 8.3,
    "summary": "After being kidnapped and imprisoned for fifteen years, Oh Dae-Su is released, only to find that he must track down his captor in five days.",
    "image": "https://m.media-amazon.com/images/M/MV5BMTI3NTQyMzU5M15BMl5BanBnXkFtZTcwMTM2MjgyMQ@@._V1_QL75_UX140_CR0,0,140,207_.jpg",
    "genres": ["Dark Comedy", "One-Person Army Action", "Psychological Thriller", "Action", "Drama"],
    "actors": ["Choi Min-sik", "Yoo Ji-tae", "Kang Hye-jeong"]
},
{
    "rank": 5,
    "title": "강남 비사이드",
    "release_year": "2024-",
    "score": 7.3,
    "summary": "In Gangnam, Seoul, Jae-Hee knows a secret about a series of disappearances but then vanishes herself. Detective Kang, outlaw Yoon, and Prosecutor Min pursue the truth for their own reasons.",
    "image": "https://m.media-amazon.com/images/M/MV5BNjgwYmJhYjgtYzJhYi00NmU5LWE1ZjEtOWRjOWJkN2M3MTU2XkEyXkFqcGc@._V1_QL75_UY207_CR3,0,140,207_.jpg",
    "genres": ["Action", "Crime", "Drama", "Mystery", "Thriller"],
    "actors": ["Jo Woo-jin", "Ji Chang-wook", "Ha Yoon-kyung"]
}
]


# ---
# 1. 장르 데이터 카운트
top_genres = count_top_genres(movies, top_n=8)

# 2. 파이 차트 생성
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
# plt.show()

# ---
# HTML 렌더링
# 이미지 데이터를 메모리에 저장
buffer = io.BytesIO()
plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')  # 고화질 설정
buffer.seek(0)  # 버퍼의 시작으로 이동

# 이미지를 Base64로 인코딩
image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
buffer.close()

# Base64 이미지를 포함한 HTML 생성
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>영화 장르 분석</title>
</head>
<body>
    <img src="data:image/png;base64,{image_base64}" alt="Pie Chart" style="display: block; margin: 0 auto; max-width: 100%;">
</body>
</html>
"""

# HTML 파일 저장
with open("genre_pie.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("HTML chart saved as 'genre_pie.html'. Open this file in a browser to view the chart.")
