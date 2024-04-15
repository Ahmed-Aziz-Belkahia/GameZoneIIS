from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.blogList, name="blog-list"),
    path('category/<slug>/', views.category_detail, name="category_detail"),
    path('<pid>', views.blogDetail, name="blog-detail"),

]
