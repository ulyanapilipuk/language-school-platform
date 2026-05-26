from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Course, Favorite, Completed, Comment, Teacher

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

    has_mentor = request.GET.get('has_mentor')
    if has_mentor == 'yes':
        courses = courses.filter(has_mentor=True)
    elif has_mentor == 'no':
        courses = courses.filter(has_mentor=False)

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

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    user = request.user
    is_favorite = False
    is_completed = False
    comments = Comment.objects.filter(course=course).order_by('-created_at')

    if user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=user, course=course).exists()
        is_completed = Completed.objects.filter(user=user, course=course).exists()

    context = {
        'course': course,
        'is_favorite': is_favorite,
        'is_completed': is_completed,
        'comments': comments,
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
def toggle_favorite(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, course=course)
    if not created:
        favorite.delete()
    return redirect('course_detail', pk=course_id)

@login_required
def toggle_completed(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    completed, created = Completed.objects.get_or_create(user=request.user, course=course)
    if not created:
        completed.delete()
    return redirect('course_detail', pk=course_id)

@login_required
def add_comment(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content and Completed.objects.filter(user=request.user, course=course).exists():
            Comment.objects.create(user=request.user, course=course, content=content)
    return redirect('course_detail', pk=course_id)

def teachers_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'courses/teachers_list.html', {'teachers': teachers})