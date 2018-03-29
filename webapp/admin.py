from django.contrib import admin
from webapp.models import questions,answer,userextend


admin.site.register(answer)
admin.site.register(questions)
admin.site.register(userextend)

# Register your models here.
