from django.shortcuts import render
from django.db.models import Q
from .models import Course

def index(request):
    return render(request, 'courses/index.html')

def course_list(request):
    courses = Course.objects.all()

    # ФИЛЬТРАЦИЯ 
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

    # СОРТИРОВКА
    sort_by = request.GET.get('sort')
    if sort_by:
        courses = courses.order_by(sort_by)
    else:
        courses = courses.order_by('-created_at')

    # ПОИСК
    search_query = request.GET.get('search')
    if search_query:
        
        matching_ids = [
            course.id for course in Course.objects.all()
            if search_query.lower() in course.title.lower()
        ]
        courses = courses.filter(id__in=matching_ids)

    return render(request, 'courses/course_list.html', {'courses': courses})

def test(request):
    return render(request, 'courses/test.html')