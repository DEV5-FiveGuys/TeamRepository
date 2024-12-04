from django.contrib import admin
from .models import *

admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Movie)
admin.site.register(Ranking)

# 이미 등록된 경우 중복 등록 방지
if MovieActor not in admin.site._registry:
    admin.site.register(MovieActor)

if MovieGenre not in admin.site._registry:
    admin.site.register(MovieGenre)