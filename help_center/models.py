from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from userauths.models import user_directory_path
from html import unescape
from django.utils.html import strip_tags
from django_ckeditor_5.fields import CKEditor5Field
from shortuuid.django_fields import ShortUUIDField


User = settings.AUTH_USER_MODEL

PUBLISH_STATUS = (
	("draft", "Draft"),
	("closed", "Closed"),
	("in_review", "In Review"),
	("published", "Published"),
)

ANSWER_STATUS = (
	("Answered", "Answered"),
	("Not Answered", "Not Answered"),
)


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title 
        
    
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to=user_directory_path)
    title = models.CharField(max_length=1000)
    content = models.TextField(null=False)
    category = models.ManyToManyField(Category, blank=True)
    tags = TaggableManager()
    status = models.CharField(choices=PUBLISH_STATUS, max_length=100, default="published")
    date = models.DateTimeField(auto_now_add=True)
    answer_status = models.CharField(choices=ANSWER_STATUS, max_length=100, default="Not Answered")
    slug = models.SlugField(unique=True)

    views = models.PositiveIntegerField(default=0)
    pid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Question "
    
    def __str__(self):
        return self.title[0:10]

    class Meta:
        ordering = ['-date']


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(null=False)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.content[0:20]


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.user