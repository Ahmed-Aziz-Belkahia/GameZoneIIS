from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.blogList, name="blog-list"),
    path('category/<str:meta_title>/', views.category_detail, name="category_detail"),
    path('<str:meta_title>', views.blogDetail, name="blog-detail"),

]
