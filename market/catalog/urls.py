from django.urls import path, include
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.CategoryListView.as_view(),
         name='category_list'),
    path('category/<slug:slug>/',
         views.CategoryDetailView.as_view(),
         name='category_detail'),
]
