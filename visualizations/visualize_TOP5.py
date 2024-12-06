from db_storage.utils import get_movies_by_country_name # db_storage.utils 에서 movies 받아오기위한 호출

# JSON 데이터에서 rank가 1~5인 영화만 필터링
def filter_top_movies(movies, max_rank=5):
    """
    JSON 데이터에서 rank값이 max_rank인 것 까지만 추출
    """
    return [movie for movie in movies if 1 <= movie['rank'] <= max_rank]

# 별점 표시 함수
def display_svg_stars(rating):
    """
    별점을 SVG 형태로 생성 (10점 만점을 5점 만점으로 변환)
    """
    rating = rating / 2
    full_star_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512" width="30" style="fill:gold;"><path d="M528.1 171.5l-146.4-21.3L316.7 17c-12.6-25.6-54.8-25.6-67.4 0l-65 132.9-146.4 21.3c-26.2 3.8-36.7 36-17.7 54.6l105.9 103-25 145.5c-4.5 26.2 23 46 46.4 33.7L288 439.6l130.6 68.6c23.4 12.3 50.9-7.4 46.4-33.7l-25-145.5 105.9-103c19-18.6 8.5-50.8-17.8-54.6z"/></svg>'
    half_star_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512" width="30" style="fill:gold;"><path d="M316.7 17L288 51.9 259.3 17c-12.6-25.6-54.8-25.6-67.4 0l-65 132.9L17 171.5C-9.2 175.3-19.6 207.5-.6 226.1l105.9 103L80.2 474.6c-4.5 26.2 23 46 46.4 33.7L288 439.6V51.9c12.6 0 25.3-12.6 28.7-17z"/></svg>'
    empty_star_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512" width="30" style="fill:lightgray;"><path d="M528.1 171.5l-146.4-21.3L316.7 17c-12.6-25.6-54.8-25.6-67.4 0l-65 132.9-146.4 21.3c-26.2 3.8-36.7 36-17.7 54.6l105.9 103-25 145.5c-4.5 26.2 23 46 46.4 33.7L288 439.6l130.6 68.6c23.4 12.3 50.9-7.4 46.4-33.7l-25-145.5 105.9-103c19-18.6 8.5-50.8-17.8-54.6z"/></svg>'
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    return full_star_svg * full_stars + half_star_svg * half_star + empty_star_svg * empty_stars

# 영화 카드 생성 함수
def create_movie_card(movie):
    """
    영화 데이터를 카드 형식 HTML로 생성 (이미지, 제목, 연도, 별점)
    """
    try:
        stars_html = display_svg_stars(float(movie['score']))
        return f"""
        <div style="display:inline-block; text-align:center; margin:10px; width:200px;">
            <img src="{movie['image']}" style="width:150px; height:200px; object-fit:cover; border:1px solid #ccc; border-radius:8px;">
            <div style="margin-top:10px; font-weight:bold;">{movie['title']}</div>
            <div style="font-size:12px; color:gray;">{movie['release_year']}</div>
            <div style="margin-top:5px;">{stars_html}</div>
        </div>
        """
    except Exception as e:
        return f"<div>Error loading movie: {e}</div>"

# 전체 영화 리스트 HTML 생성 및 저장
def save_movies_html(movies, filename="TOP5_movies.html"):
    """
    영화 데이터를 HTML 파일로 저장 (카드 형식으로 정렬)
    """
    filtered_movies = filter_top_movies(movies)
    movie_cards = ''.join([create_movie_card(movie) for movie in filtered_movies])
    html = f"""
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
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)
    print(f"HTML file saved as '{filename}'. Open it in a browser to view the result.")

# 전체 영화 리스트 HTML 생성 및 저장
def save_movies_html(movies, filename="TOP5_movies.html"):
    """
    영화 데이터를 HTML 파일로 저장 (카드 형식으로 정렬)
    """
    filtered_movies = filter_top_movies(movies)
    movie_cards = ''.join([create_movie_card(movie) for movie in filtered_movies])
    html = f"""
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
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)
    print(f"HTML file saved as '{filename}'. Open it in a browser to view the result.")

# ---------------------------------
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

name = "kr"  # korea movies 받아오기
movies = get_movies_by_country_name(name)

# 실행
save_movies_html(movies)



