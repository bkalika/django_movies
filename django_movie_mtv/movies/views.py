from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .forms import ReviewForm
from .models import Movie, Actor


class MovieView(ListView):
    """List of movies"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)

    # template_name = "movies/movie_list.html"
    # !!!instead of template_name we can rename out html file (movie.html) to
    # "movie_list.html" and Django itself to adds suffix _list and find out file. Amazing!!!
    # instead of method get, we create ListView:
    # def get(self, request):
    #     movies = Movie.objects.all()
    #     return render(request, "movies/movie_list.html", {"movie_list": movies})


class MovieDetailView(DetailView):
    """Full description of film"""
    model = Movie
    slug_field = "url"

    # !!!we do not have parameter "template_name" (movie_detail.html) due to
    # Django itself to adds suffix _detail and find out file. Amazing!!!


class AddReview(View):
    """Review"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(DetailView):
    model = Actor
    template_name = "movies/actors.html"
    slug_field = "name"
