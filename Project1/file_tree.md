Project1/
├── Project1
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── WebCrawling
│   ├── __init__.py
│   ├── data
│   │   └── raw
│   │       ├── country_code.json
│   │       ├── movies_data.json
│   │       └── movies_data_country.json
│   ├── requirements_YJ.txt
│   └── src
│       ├── __init__.py
│       └── utils.py
├── db_storage
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_remove_country_code.py
│   │   ├── 0003_alter_movie_score.py
│   │   ├── 0004_alter_movie_score.py
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── extract_file_directory.py
├── manage.py
└── visualizations
    ├── TOP5_movies.html
    ├── __pycache__
    │   └── visualize_TOP5.cpython-313.pyc
    ├── average_rating.html
    ├── film_camera_mask.png
    ├── genre_pie.html
    ├── visualize_TOP5.py
    ├── visualize_averagerating.py
    ├── visualize_piechart.py
    ├── visualize_wordcloud.py
    └── wordcloud.html