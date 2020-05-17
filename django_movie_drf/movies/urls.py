from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .import api
from .import views

urlpatterns = format_suffix_patterns([
    path('movie/', views.MovieViewSet.as_view({'get': 'list'})),
    path('movie/<int:pk>/', views.MovieViewSet.as_view({'get': 'retrieve'})),
    path('review/', views.ReviewCreateViewSet.as_view({'post': 'create'})),
    path('rating/', views.AddStarRatingViewSet.as_view({'post': 'create'})),
    path('actor/', views.ActorsViewSet.as_view({'get': 'list'})),
    path('actor/<int:pk>/', views.ActorsViewSet.as_view({'get': 'retrieve'})),
])


###########
# router = DefaultRouter()
# router.register(r'actor-set', api.ActorViewSet, basename='actor')
# router.register(r'actor-read', api.ActorReadOnly, basename='actor')

# urlpatterns = [
#     path('movie/', views.MovieListView.as_view()),
#     path('movie/<int:pk>/', views.MovieDetailView.as_view()),
#     path('review/', views.ReviewCreateView.as_view()),
#     path('rating/', views.AddStarRatingView.as_view()),
#     # path('actors/', views.ActorsListView.as_view()),
#     path('actors/', views.ActorViewSet.as_view({'get': 'list'})),
#     # path('actors/<int:pk>', views.ActorDetailView.as_view()),
#     path('actors/<int:pk>', views.ActorViewSet.as_view({'get': 'retrieve'})),
# ]
