from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from userauths.models import user_directory_path
from html import unescape
from django.utils.html import strip_tags
from django_ckeditor_5.fields import CKEditor5Field
from shortuuid.django_fields import ShortUUIDField


User = settings.AUTH_USER_MODEL

BLOG_PUBLISH_STATUS = (
	("draft", "draft"),
	("in_review", "In Review"),
	("published", "Published"),
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
        
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to=user_directory_path)
    title = models.CharField(max_length=1000)
    content = CKEditor5Field(config_name='extends')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = TaggableManager()
    status = models.CharField(choices=BLOG_PUBLISH_STATUS, max_length=100, default="in_review")
    featured = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    pid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")

    class Meta:
        verbose_name = "Posts"
        verbose_name_plural = "Posts "
    
    def __str__(self):
        return self.title[0:10]

    class Meta:
        ordering = ['-date']

    def get_read_time(self):
        string = self.content + unescape(strip_tags(self.content))
        total_words = len((string).split())

        return round(total_words / 200)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    full_name = models.CharField(max_length=1000)
    email = models.EmailField()
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.comment[0:20]
