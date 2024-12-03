from django.db import models

# Create your models here.
class Country(models.Model):
    code = models.CharField(max_length=10, unique=True) # ISO country code
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.CharField(max_length=20)  # TODO: DateField or DateTimeField
    score = models.DecimalField(max_digits=3, decimal_places=1)
    summary = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, through='MovieGenre', related_name='movies')
    actors = models.ManyToManyField(Actor, through='MovieActor', related_name='movies')

    """def __str__(self):
        return {
            'title': self.title,
            'release_year': self.release_year,
            'score': self.score,
            'summary': self.summary,
            'image_url': self.image_url,
            'genres': self.genres,
            'actors': self.actors
        }"""
    def __str__(self):
        genres = ', '.join([genre.name for genre in self.genres.all()])
        actors = ', '.join([actor.name for actor in self.actors.all()])
        return f"Title: {self.title}, Release Year: {self.release_year}, Score: {self.score}, Genres: {genres}, Actors: {actors}"




class MovieGenre(models.Model):
    '''
        Movie_Genre Join Table
            - movie: int - movie table PK
            - genre: int - genre table PK
    '''
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('movie', 'genre')

    def __str__(self):
        # Movie와 Genre의 이름을 연결한 문자열을 반환
        return f"{self.movie.title} - {self.genre.name}"
        

class MovieActor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('movie', 'actor')
    
    def __str__(self):
        # Movie와 Genre의 이름을 연결한 문자열을 반환
        return f"{self.movie.title} - {self.actor.name}"


class Ranking(models.Model):
    
    country = models.ForeignKey("Country", on_delete=models.CASCADE)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    rank = models.PositiveSmallIntegerField()
    
    class Meta:
        unique_together = ('country', 'rank')
    
    def __str__(self):
        return f'{self.country.name} - {self.rank} - {self.movie.title}'