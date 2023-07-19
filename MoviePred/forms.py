from django import forms
from .models import Review, Movie

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']
class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = ['movie_id', 'title', 'description', 'genre', 'date_released']

