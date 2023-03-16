from django.urls import path
from houses import views


urlpatterns = [
    path('houses/', views.HouseList.as_view()),
]