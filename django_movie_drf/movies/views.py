from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer
from .models import Movie


class MovieListView(APIView):
    """Showing the list of movies"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """Showing description of movie"""

    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """Add review to movie"""

    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)
