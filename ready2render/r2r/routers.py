from django.urls import path
from . import views
from .views import CombineView

urlpatterns = [
    path('combine_nfts/', CombineView.as_view(), name="combine-view")
]