from django.urls import path
from . import views

urlpatterns = [
        path("", views.home_view, name="home"),
        path("muller-report/question-and-answers/<slug:slug>/", views.QuestionAnswerView.as_view(), name="questions"),
        ]
