from django.shortcuts import render


def home_view(request):
    return render(request, "reportapp/home.html")

# TODO Create Views.
# TODO Are views going to be class based , function based or a mixture of both
# TODO Create docstrings in all views for documentation.
# TODO For Views, create QuerySets - Look up in Django Documentation.
