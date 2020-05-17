from django.db import models
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .utils import get_client_ip, MovieFilter
from .serializers import (MovieListSerializer,
                          MovieDetailSerializer,
                          ReviewCreateSerializer,
                          CreateRatingSerializer,
                          ActorListSerializer,
                          ActorDetailSerializer,
                          )
from .models import Movie, Actor


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Output list of movie"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F("ratings__star")) / models.Count(models.F("ratings"))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Adding the review to movie"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Adding the rating to movie"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
    """Output the actors or directors"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == 'retrieve':
            return ActorDetailSerializer


# """For generics:"""
#
#
# class MovieListView(generics.ListAPIView):
#     """Showing the list of movies"""
#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = MovieFilter
#     permission_classes = [permissions.IsAuthenticated]
#
#     # def get(self, request):
#     #     movies = Movie.objects.filter(draft=False).annotate(
#     #         rating_user=models.Case(
#     #             models.When(ratings__ip=get_client_ip(request), then=True),
#     #             default=False,
#     #             output_field=models.BooleanField()
#     #         ),
#     #     )
#
#     """if we inherit from APIView, then:"""
#     # def get(self, request):
#     #     movies = Movie.objects.filter(draft=False).annotate(
#     #         rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
#     #     ).annotate(
#     #         middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
#     #     )
#     #     serializer = MovieListSerializer(movies, many=True)
#     #     return Response(serializer.data)
#
#     """ListApiView"""
#     def get_queryset(self):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count("ratings",
#                                      filter=models.Q(ratings__ip=get_client_ip(self.request)))
#         ).annotate(
#             middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
#         )
#         return movies
#
#
# class MovieDetailView(generics.RetrieveAPIView):
#     """Showing description of movie"""
#
#     """if we inherit from APIView, then:"""
#     # def get(self, request, pk):
#     #     movie = Movie.objects.get(id=pk, draft=False)
#     #     serializer = MovieDetailSerializer(movie)
#     #     return Response(serializer.data)
#
#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer
#
#
# class ReviewCreateView(generics.CreateAPIView):
#     """Add review to movie"""
#
#     """if we inherit from APIView, then:"""
#     # def post(self, request):
#     #     review = ReviewCreateSerializer(data=request.data)
#     #     if review.is_valid():
#     #         review.save()
#     #     return Response(status=201)
#
#     serializer_class = ReviewCreateSerializer
#
#
# class AddStarRatingView(generics.CreateAPIView):
#     """
#     add rank to object
#     """
#     """if we inherit from APIView, then:"""
#     # def post(self, request):
#     #     serializer = CreateRatingSerializer(data=request.data)
#     #     if serializer.is_valid():
#     #         serializer.save(ip=get_client_ip(request))
#     #         return Response(status=201)
#     #     else:
#     #         return Response(status=400)
#
#     serializer_class = CreateRatingSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))
#
#
# class ActorsListView(generics.ListAPIView):
#     """Output list of actors"""
#     queryset = Actor.objects.all()
#     serializer_class = ActorListSerializer
#
#
# class ActorDetailView(generics.RetrieveAPIView):
#     """Output actors or directors"""
#     queryset = Actor.objects.all()
#     serializer_class = ActorDetailSerializer
