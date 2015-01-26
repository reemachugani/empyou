from django.contrib import admin
from models import Answer, Question

class QuestionAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)