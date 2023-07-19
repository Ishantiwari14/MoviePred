from rest_framework import generics,views,permissions, status
from MoviePred.models import Movie,Review
from django.shortcuts import render, get_object_or_404, redirect
from .serializers import MovieSerializer, ReviewSerializer
from MoviePred.sentiment_predictor import sentiment_predictor,get_probabilities
from .owner_permission import IsOwnerOrReadOnly
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from MyAuth.models import UserProfile
from django.db.models import Avg,Count
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth.models import User
from collections import defaultdict
import numpy as np
from django.shortcuts import render
from random import sample
from django.shortcuts import render, get_object_or_404
from .forms import ReviewForm,MovieForm
# from MoviePred.recommender import find_similar_users
from django.contrib.auth.decorators import login_required

class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    def perform_create(self, serializer):
        serializer.save(movie_owner = self.request.user)
    
class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsOwnerOrReadOnly ,permissions.IsAuthenticatedOrReadOnly,]

class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_update(self, serializer):

        review = self.get_object()
        if review.user != self.request.user:
            raise PermissionDenied("You are not the author of this review")
        
        serializer.save()

    def perform_destroy(self, instance):

        if instance.user != self.request.user:
            raise PermissionDenied("You are not the author of this review.")
        
        instance.delete()

class MovieReviewListCreate(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]


    def get_queryset(self):
        movie_id = self.kwargs['pk']
        queryset = Review.objects.filter(movie_id = movie_id)
        return queryset

    def perform_create(self, serializer):
        movie_id = self.kwargs['pk']
        movie = generics.get_object_or_404(Movie, pk=movie_id)

        review_text = self.request.data.get('content', '')
        user = self.request.user
        critic_name = f"{user.first_name} {user.last_name}"
        sentiment_pred = sentiment_predictor(review_text)
        probabilities = get_probabilities(review_text)
        prob_pos = probabilities[0][1]
        prob_neg = probabilities[0][0]
        serializer.validated_data['critic_name'] = critic_name
        serializer.validated_data['sentiment_pred'] = sentiment_pred
        serializer.validated_data['movie'] = movie

        serializer.save(user=self.request.user, movie=movie, sentiment_pred=sentiment_pred, prob_pos=prob_pos, prob_neg=prob_neg)


class MovieRecommendationView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        try:
            profile = user.profile
            genre_preferences = profile.genre_preferences.all()

            recommended_movies = Movie.objects.filter(genre__in=genre_preferences).annotate(avg_rating=Avg('review__rating'))

            recommended_movies = recommended_movies.filter(avg_rating__gte=4.0)

            serializer = MovieSerializer(recommended_movies, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response([]);

def index(request):
    query = request.GET.get('query')
    user = request.user
    if request.user.is_authenticated:
        print("USER IS AUTHENTICATED")
        # User is logged in
        # Perform actions for logged-in users
        user = request.user
        # ... do something with the user ...
        profile = user.profile

        genre_preferences = profile.genre_preferences.all()

        recommended_movies = Movie.objects.filter(
        genre__in=genre_preferences,
        review__rating__gt=4
        ).annotate(avg_rating=Avg('review__rating'))[:10]


        print(recommended_movies)
    else:
        recommended_movies = Movie.objects.all()
       
    if query:
        # Perform a case-insensitive search for movies that contain the query in their title
        movies = Movie.objects.filter(title__icontains=query)
    else:
        # Get 5 random movies if no search query is provided
        movies = sample(list(Movie.objects.all()), 5)
        print(movies)
    context = {
        'movies': movies,
        'query': query,
        'recommend': recommended_movies
    }

    return render(request, 'index.html', context)

def movie_details(request, pk):
    # Get the movie with the specified movie_id
    movie = get_object_or_404(Movie, pk=pk)

    context = {
        'movie': movie,
        'user': request.user
    }

    return render(request, 'movie_details.html', context)

def add_review(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    print("ADD REVIEW INIT")
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        print("checking if form valid")
        review = form.save(commit=False)
        review.critic_name = request.user
        review.movie = movie
        review.user = request.user
        review_text = review.content
        print("REVIEWW TEXT")
        print(review_text)
        #critic_name = f"{user.first_name} {user.last_name}"
        sentiment_pred = sentiment_predictor(review_text)
        probabilities = get_probabilities(review_text)
        prob_pos = probabilities[0][1]
        prob_neg = probabilities[0][0]
        review.sentiment_pred = sentiment_pred
        review.prob_pos = prob_pos
        review.prob_neg = prob_neg
        review.save()
        
        return redirect('movie_details', pk=pk)
    else:
        form = ReviewForm()
    
    context = {
        'movie': movie,
        'form': form
    }
    
    return render(request, 'add_review.html', context)

@login_required
def add_movie(request):
    print("ADD MOVIES INIT")
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.movie_owner = request.user      
            movie.save()

            return redirect('index')  # Replace 'movie_list' with the URL name of your movie list page
    else:
        form = MovieForm()

    return render(request, 'add_movie.html', {'form': form})