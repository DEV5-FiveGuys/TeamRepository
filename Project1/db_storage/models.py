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
    score = models.DecimalField(max_digits=3, decimal_places=1)
    summary = models.TextField()
    poster_url = models.URLField()
    genres = models.ManyToManyField(Genre, through='MovieGenre', related_name='movies')
    actors = models.ManyToManyField(Actor, through='MovieActor', related_name='movies')

    def __str__(self):
        return {
            'title': self.title,
            'score': self.score,
            'summary': self.summary,
            'poster_url': self.poster_url,
            'genres': self.genres,
            'actors': self.actors
        }


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
        

class MovieActor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('movie', 'actor')
        
class Ranking(models.Model):
    country = models.ForeignKey("Country", on_delete=models.CASCADE)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    rank = models.PositiveSmallIntegerField()
    
    class Meta:
        unique_together = ('country', 'rank')
    
    def __str__(self):
        return f'{self.country.name} - {self.rank} - {self.movie.title}'