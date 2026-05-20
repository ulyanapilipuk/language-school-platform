from django.contrib import admin

# Register your models here.
from .models import Course, Favorite, Completed, Comment

admin.site.register(Course)
admin.site.register(Favorite)
admin.site.register(Completed)
admin.site.register(Comment)