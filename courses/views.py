from django.shortcuts import render
from django.db.models import Q
from .models import Course

def index(request):
    return render(request, 'courses/index.html')

def course_list(request):
    courses = Course.objects.all()

    # Поиск по названию
    search_query = request.GET.get('search')
    if search_query:
        courses = courses.filter(title__icontains=search_query)

    # Фильтрация
    difficulty = request.GET.get('difficulty')
    if difficulty:
        courses = courses.filter(difficulty=difficulty)

    course_type = request.GET.get('type')
    if course_type:
        courses = courses.filter(type=course_type)

    price_filter = request.GET.get('price')
    if price_filter == 'free':
        courses = courses.filter(price=0)
    elif price_filter == 'paid':
        courses = courses.filter(price__gt=0)

    has_mentor = request.GET.get('has_mentor')
    if has_mentor == 'yes':
        courses = courses.filter(has_mentor=True)
    elif has_mentor == 'no':
        courses = courses.filter(has_mentor=False)

    # Сортировка
    sort_by = request.GET.get('sort')
    if sort_by:
        courses = courses.order_by(sort_by)
    else:
        courses = courses.order_by('-created_at')  # по умолчанию сначала новые

    return render(request, 'courses/course_list.html', {'courses': courses})