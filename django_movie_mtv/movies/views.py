from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .forms import ReviewForm, RatingForm
from .models import Movie, Actor, Genre, Rating


class GenreYear:
    """Genres and years of release"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MovieView(GenreYear, ListView):
    """List of movies"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 2

    # template_name = "movies/movie_list.html"
    # !!!instead of template_name we can rename out html file (movie.html) to
    # "movie_list.html" and Django itself to adds suffix _list and find out file. Amazing!!!
    # instead of method get, we create ListView:
    # def get(self, request):
    #     movies = Movie.objects.all()
    #     return render(request, "movies/movie_list.html", {"movie_list": movies})


class MovieDetailView(GenreYear, DetailView):
    """Full description of film"""
    model = Movie
    slug_field = "url"

    # !!!we do not have parameter "template_name" (movie_detail.html) due to
    # Django itself to adds suffix _detail and find out file. Amazing!!!

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context


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


class ActorView(GenreYear, DetailView):
    model = Actor
    template_name = "movies/actors.html"
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    """Filter of movies"""
    paginate_by = 1

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join(f'year={x}&' for x in self.request.GET.getlist("year"))
        context["genre"] = ''.join(f'genre={x}&' for x in self.request.GET.getlist("genre"))
        return context


class JsonFilterMoviesView(ListView):
    """Filter of movies in JSON"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)


class AddStarRating(View):
    """Add rating for movie"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    """Search movies"""
    paginate_by = 3

    def get_queryset(self):
        search_query = self.request.GET.get('q', None)
        if search_query:
            return Movie.objects.filter(title__icontains=search_query)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context
