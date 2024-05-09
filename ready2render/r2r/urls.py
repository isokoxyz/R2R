from django.urls import path
from . import views
from views import CombineView

urlpatterns = [
    path("", views.index, name="index"),
    path("combine_nfts/", CombineView.as_view())
]