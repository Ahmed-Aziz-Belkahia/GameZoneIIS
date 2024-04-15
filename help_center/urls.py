from django.urls import path
from help_center import views

app_name = 'help-center'

urlpatterns = [
    path('', views.question_list, name="list"),
    path('detail/<slug:slug>/', views.question_detail, name="detail"),


    path('mark_as_answered/', views.mark_as_answered, name="mark_as_answered"),
    path('mark_as_not_answered/', views.mark_as_not_answered, name="mark_as_not_answered"),
    path('mark_noti_as_seen/', views.mark_noti_as_seen, name="mark_noti_as_seen"),
    path('answer_question/', views.answer_question, name="answer_question"),

]
