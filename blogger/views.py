from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string
from datetime import date
from .models import post, Review, Files
from django.db.models import Avg, Max, Min
from .forms import BlogForm, FileForm, CommentForm
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView


# Create your views here.

all_posts = []


class Welcome(ListView):
    template_name = "blogger/welcome.html"
    model = post
    context_object_name = "posts"
    ordering = [
        "-date",
    ]

    def get_queryset(self):
        base = super().get_queryset()
        return base[:2]





class ALLPost(ListView):
    template_name = "blogger/allPost.html"
    model = post
    context_object_name = "all_posts"
    ordering = ["-date"]




class MyPost(View):
    template_name = "blogger/myPost.html"
    model = post

    def get(self, request, slug):
        p = get_object_or_404(post, slug=slug)
        stored_post = request.session.get('stored_post')
        is_stored = False
        if stored_post is not None:
            if p.id in stored_post:
                is_stored = True
       

        form = CommentForm()

        return render(
            request,
            "blogger/myPost.html",
            {
                "post": p,
                "tags": p.tags.all(),
                "comment_form": form,
                "comments": p.comments.all().order_by("-date"),
                "is_stored":is_stored
            },
        )

    def post(self, request, slug):
        p = post.objects.get(slug=slug)
        stored_post = request.session.get('stored_post')
        if stored_post is not None:
            is_stored = p.id in stored_post
        else:
            is_stored = False

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = p
            comment.save()
            redirect_url = reverse("ind_post", kwargs={"slug": slug})
            return HttpResponseRedirect(redirect_url)

        return render(
            request,
            "blogger/myPost.html",
            {"post": p, "tags": p.tags.all(), "comment_form": form,'is_stored': is_stored},
        )


class ReadLaterView(View):
    def get(self, request):
        stored_post = request.session.get("stored_post")

        context = {}
        if stored_post is None or len(stored_post) == 0:
            context["store_post"] = []
            context["has_post"] = False
        else:
            posts = post.objects.filter(id__in=stored_post)
            context["store_post"] = posts
            context["has_post"] = True
        return render (request,"blogger/readlater.html",context)

    def post(self, request):
        stored_post = request.session.get("stored_post")

        if stored_post is None:
            stored_post = []

        post_id = request.POST["post_id"]
        if post_id not in stored_post:
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)
        request.session['stored_post'] = stored_post


        return HttpResponseRedirect("/")


# def myPost(request, slug):
#     p = get_object_or_404(post, slug=slug)

#     return render(request, "blogger/myPost.html", {"post": p, "tags": p.tags.all()})





class FileListView(ListView):
    template_name = "blogger/FileList.html"
    model = Files
    context_object_name = "files"


class CreateFileView(CreateView):
    template_name = "blogger/files.html"
    model = Files
    fields = "__all__"
    success_url = "/thanks"


class CreateProfileView(View):
    def get(self, request):
        form = FileForm()
        return render(request, "blogger/files.html", {"form": form})

    def post(self, request):
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = Files(image=request.FILES["user_image"])
            file.save()
            print(request.FILES["user_image"])
            return HttpResponseRedirect("/file")
        return render(request, "blogger/files.html", {"form", form})


class form(FormView):
    form_class = BlogForm
    template_name = "blogger/test_form.html"
    success_url = "/thanks"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)



class Thanks(TemplateView):
    # def get(self, request):
    #     return render(request, "blogger/thanks.html")
    template_name = "blogger/thanks.html"

    def get_context_data(self, **kwargs: Any):
        # must call the get_context_data() in the template view
        context = super().get_context_data(**kwargs)
        context["name"] = "David"
        return context


class RListView(ListView):
    template_name = "blogger/list.html"
    model = Review
    context_object_name = "reviews"

    def get_queryset(self):
        base = super().get_queryset()
        query = base.filter(rate__gt=3)
        return query



class ReviewsView(DetailView):
    template_name = "blogger/single_reviews.html"
    model = Review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        laoded = self.object
        request = self.request
        fav = request.session.get("favorite_review")
        context["is_favorite"] = fav == str(laoded.id)
        return context


class FavoriteView(View):
    def post(self, request):
        review_id = request.POST["review_id"]
        # fav_review = Review.objects.get(pk=review_id)
        request.session["favorite_review"] = review_id
        redirect_url = reverse("single_review", kwargs={"pk": review_id})
        return HttpResponseRedirect(redirect_url)




def test(request):
    posts = post.objects.all().order_by("-rating")
    num_post = posts.count()
    avg_rating = posts.aggregate(Avg("rating"))
    return render(
        request,
        "blogger/test.html",
        {"posts": posts, "number_of_post": num_post, "average_rating": avg_rating},
    )


def test_detail(request, slug):
    # most specify the attribute
    p = get_object_or_404(post, slug=slug)

    return render(request, "blogger/test_detail.html", {"post": p})
