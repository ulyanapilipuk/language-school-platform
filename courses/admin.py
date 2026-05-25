from django.contrib import admin
from .models import Course, Favorite, Completed, Comment, Teacher

admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Favorite)
admin.site.register(Completed)
admin.site.register(Comment)