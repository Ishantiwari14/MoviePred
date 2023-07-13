from rest_framework import generics,viewsets,permissions, status
from MoviePred.models import Movie,Review
from .serializers import MovieSerializer, ReviewSerializer
from MoviePred.sentiment_predictor import sentiment_predictor
from .owner_permission import IsOwnerOrReadOnly
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response

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
        serializer.validated_data['critic_name'] = critic_name
        serializer.validated_data['sentiment_pred'] = sentiment_pred
        serializer.validated_data['movie'] = movie

        serializer.save(user=self.request.user, movie=movie, sentiment_pred=sentiment_pred)


class MovieRecommendationView(generics.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user

        genre_preferences = user.genre_preferences.all()

        recommended_movies = Movie.objects.filter(genre__in=genre_preferences)

        recommended_movies = recommended_movies.order_by('-rating')

        serializer = MovieSerializer(recommended_movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)