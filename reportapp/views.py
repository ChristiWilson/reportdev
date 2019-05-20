from django.shortcuts import render
from django.views.generic import DetailView

from .models import Question, QAText


def home_view(request):
    return render(request, "reportapp/home.html")


class QuestionAnswerView(DetailView):
    model = Question
    template_name = "reportapp/questions.html"
    # context_object_name = "questions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the text for the q & a
        context["questions"] = Question.objects.all()
        context["questexts"] = QAText.objects.exclude(qa_choice="A")
        context["anstext"] = QAText.objects.filter(qa_choice="A")
        return context


# TODO Create Views.
# TODO Are views going to be class based , function based or a mixture of both
# TODO Create docstrings in all views for documentation.
# TODO For Views, create QuerySets - Look up in Django Documentation.


