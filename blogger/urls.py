from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
   
    path("file",views.CreateFileView.as_view()),
    path("filelist",views.FileListView.as_view()),
    path("form",views.form.as_view(), name=""),
    path("thanks",views.Thanks.as_view(), name=""),
    path("review/favorite",views.FavoriteView.as_view()),
    path("reviews",views.RListView.as_view()),
    path("reviews/<int:pk>",views.ReviewsView.as_view(),name = "single_review"),
    path("",views.Welcome.as_view(), name="welcome_page"),
    path("posts",views.ALLPost.as_view(), name= "postList"),
    path("posts/test",views.test),
    path("posts/test/<slug:slug>",views.test_detail,name="test_detail"),
    path("posts/read-later,views",views.ReadLaterView.as_view(), name="read_later"),
    path("posts/<slug:slug>",views.MyPost.as_view(), name="ind_post")


]