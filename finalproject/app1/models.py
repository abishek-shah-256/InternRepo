from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
# from profiles.models import Profile


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    bio_info= models.TextField(max_length=300, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Post(models.Model):
    content = models.CharField(max_length=500, blank=False)
    author = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)   
    created_at = models.DateTimeField(auto_now_add=True)
    post_img = models.ImageField(upload_to="post_img/", null=True)
    num_likes = models.IntegerField(default=0)


    def __str__(self):
        return self.content
    
    class Meta:
        ordering = ['-created_at']



class Likes(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_like = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)

    def __str__(self):
        return self.num_likes



class Comment(models.Model):
    comment_content = models.CharField(max_length=500, blank=True)
    comment_date = models.DateTimeField(auto_now_add=True)
    commented_user = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    comment_post = models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_content[:20]


