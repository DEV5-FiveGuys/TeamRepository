from statistics import mean
from visualize_TOP5 import display_svg_stars # TOP5 시각화 코드에서 함수 호출
from db_storage.utils import get_movies_by_country_name # db_storage.utils 에서 movies 받아오기위한 호출

# 평균 별점 계산
def calculate_average_rating(movies):
    """
    전체 영화의 평균 별점 계산 (10점 만점을 기준으로 입력됨)
    """
    scores = [float(movie['score']) for movie in movies]
    return mean(scores)

# HTML로 평균 별점 표시
def display_average_rating_in_html(movies):
    """
    평균 별점을 HTML로 렌더링
    """
    avg_rating = calculate_average_rating(movies)
    svg_stars = display_svg_stars(avg_rating)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Average Movie Rating</title>
    </head>
    <body>
        <h1 style="text-align: center;">Average Rating: {avg_rating:.1f}/10</h1>
        <div style="text-align: center;">{svg_stars}</div>
    </body>
    </html>
    """
    with open("average_rating.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    print("HTML file 'average_rating.html' has been saved.")

# 테스트 데이터
'''
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
'''

# "South Korea"로 영화 데이터를 가져옴
name = "South Korea"
movies = get_movies_by_country_name(name)

# 실행
display_average_rating_in_html(movies)
