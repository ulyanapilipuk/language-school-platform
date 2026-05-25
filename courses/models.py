from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]
    AGE_GROUP_CHOICES = [
        ('children', 'Дети'),
        ('teen', 'Подростки'),
        ('adult', 'Взрослые'),
    ]
    TYPE_CHOICES = [
        ('audio', 'Аудио'),
        ('text', 'Текст'),
        ('video', 'Видео'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    content = models.TextField(verbose_name='Содержание')
    video_url = models.CharField(max_length=255, blank=True, null=True)
    audio_url = models.CharField(max_length=255, blank=True, null=True)
    exercises = models.TextField(blank=True, null=True)

    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    age_group = models.CharField(max_length=20, choices=AGE_GROUP_CHOICES)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    has_mentor = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    teacher = models.ForeignKey(
        'Teacher', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Преподаватель',
        related_name='courses'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

class Completed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.course.title}'


class Teacher(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    photo_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ссылка на фото')
    bio = models.TextField(verbose_name='Биография', help_text='Образование, опыт, достижения')
    experience = models.CharField(max_length=200, blank=True, null=True, verbose_name='Опыт работы')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'