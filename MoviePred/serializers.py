from rest_framework import serializers
from .models import Movie, Review, Genre
from rest_flex_fields import FlexFieldsModelSerializer
from django.contrib.auth.models import User


class GenreSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']
        expandable_fields = {
            'movies': ('MoviePred.MovieSerializer', {'many': True})
        }

class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']



class MovieSerializer(FlexFieldsModelSerializer):
    # reviews = ReviewSerializer(
    #     many = True,
    # )
    # genre = GenreSerializer(many = True)
    class Meta:
        model = Movie
        fields = (
            'id','title','description','date_released','movie_owner'
        )
        expandable_fields = {
            'reviews': ('MoviePred.ReviewSerializer', {'many': True}),
            'genre' : (GenreSerializer, {'many': True})
        }
        read_only_fields = ('movie_owner',)

class ReviewSerializer(FlexFieldsModelSerializer):
    movie = MovieSerializer
    class Meta: 
        model = Review
        fields = (
            'id', 'content','rating','critic_name','movie','review_date', 'sentiment_pred','user'
        )
        read_only_fields = ('id', 'sentiment_pred', 'movie', 'review_date','user','critic_name')