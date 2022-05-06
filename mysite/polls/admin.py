from django.contrib import admin


from polls.models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model=Choice
    extra=3
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text","pub_date")
    fieldsets = [
        (None, {
            "fields":['pub_date']
        }),
        ('Question Information', {"fields":['question_text']}),
    ]
    inlines=[ChoiceInline]
    
    #fields = ["pub_date", "question_text"]

admin.site.register(Question, QuestionAdmin)

# Register your models here.
