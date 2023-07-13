from django.db.models.signals import post_save
from django.dispatch import receiver
from app1.models import CustomUser
from .models import Profile, Relationship


@receiver(post_save, sender=CustomUser)
def post_save_create_profile(sender,instance,created, **kwargs):
   if created:
      Profile.objects.create(first_name=instance.first_name,
                             last_name=instance.last_name,
                             email=instance.email,
                             gender=instance.gender,
                             user=instance,
                             )



@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
   sender_ = instance.sender
   receiver_ = instance.receiver

   if instance.status == 'accepted':
      sender_.friends.add(receiver_.user)
      receiver_.friends.add(receiver_.user)
      sender_.save() 
      receiver_.save()


   if instance.status == 'rejected':
      instance.delete()




