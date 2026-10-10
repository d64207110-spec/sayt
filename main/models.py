from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Topic(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField('Аватарка', upload_to='avatars/', blank=True, null=True)
    about = models.TextField('Обо мне', max_length=1000, blank=True,
                             help_text='Расскажи о себе: что любишь, чем увлекаешься и т.д.')

    def __str__(self):
        return f'Профиль {self.user.username}'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)