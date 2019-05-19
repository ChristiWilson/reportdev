from django.contrib import admin

from .models import Question, QAText


class QATextInline(admin.StackedInline):
    model = QAText
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
            ("Part and Category", {
                    "fields": (
                            ("category", "part"), "title",
                            ),
                    }
             ),
            ]
    inlines = [
            QATextInline,
            ]


admin.site.register(Question, QuestionAdmin)

# TODO Create Docstring to document the admin layout.
