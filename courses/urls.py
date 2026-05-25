from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('toggle_favorite/<int:course_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('toggle_completed/<int:course_id>/', views.toggle_completed, name='toggle_completed'),
    path('add_comment/<int:course_id>/', views.add_comment, name='add_comment'),
    path('teachers/', views.teachers_list, name='teachers_list'),
]