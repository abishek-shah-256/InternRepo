from django.db import models
from app1.models import CustomUser
from profiles.utils import get_random_code
from django.template.defaultfilters import slugify



class Profile(models.Model):
    first_name = models.CharField(max_length=50,blank=True, null=True)
    last_name = models.CharField(max_length=50,blank=True, null=True)
    email = models.EmailField(unique=True, blank=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatar.png',upload_to='profile/')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    friends = models.ManyToManyField(CustomUser, blank= True, related_name='friends')
    bio_info= models.TextField(max_length=300, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    last_online = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        # return f"{self.user.email} -- {self.created}.strftime('%d-%m-%Y')"
        return f"{self.user.email}"
    
    def profiles_posts(self):
        return self.post_set.all()
    
    # def friends_posts(self):
    #     friends = self.friends.all()
    #     friends_post = 'app1.Post'.objects.filter(user=friends)
    #     return friends_post
    

    def get_friends(self): 
        # return self.friends.all()
        return self.friends.exclude(profile = self.user.profile)

    
    def get_friends_no(self):
        # return self.friends.all().count()
        return self.friends.exclude(profile = self.user.profile).count()
    
    def save(self, *args, **kwargs):
        ex = False
        print(get_random_code())
        if self.first_name and self.last_name:
            to_slug =  slugify(str(self.first_name) + " "+ str(self.last_name +" "+ str(get_random_code() )))
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Profile.objects.filter(slug=to_slug).exists()

        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status="send")
        return qs
    

class Relationship(models.Model):
    STATUS_CHOICES = (
        ('send', 'send'),
        ('accepted', 'accepted'),
        ('waiting','waiting'),
        ('rejected','rejected'),
        )
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"sender = {self.sender}-\n nreceiver = {self.receiver}\n{self.status}"
    




