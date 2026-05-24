import re
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

def validate_belarus_phone(value):
    if not value:
        return  # пустое значение допустимо
    pattern = r'^\+375(29|33|44|25)\d{7}$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Номер телефона должен быть в формате +375 (29/33/44/25) и 7 цифр, например +375291234567'
        )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[validate_belarus_phone],
        verbose_name='Телефон'
    )
    

    def __str__(self):
        return f'Профиль {self.user.username}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()