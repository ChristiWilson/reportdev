from django.contrib import admin

from .models import Question, QAText


class QATextInline(admin.StackedInline):
    model = QAText
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
            ("Part and Category", {
                    "fields": (
                            ("category", "part"), "title", "slug"
                            ),
                    }
             ),
            ]
    inlines = [
            QATextInline,
            ]
    prepopulated_fields = {"slug": ("title",)}
    # autocomplete_fields = {"slug": "title"}


admin.site.register(Question, QuestionAdmin)

# TODO Create Docstring to document the admin layout.
# TODO For Testing purposes, create Admin views for all models
