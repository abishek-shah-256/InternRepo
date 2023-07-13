from django.shortcuts import render,redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from profiles.models import Profile, Relationship


def myProfile(request):
    obj = Profile.objects.get(user=request.user)
    context = {
        'obj': obj,
    }

    return render(request,'profiles/profile.html',context)


def editProfile(request,pk):
    obj = Profile.objects.get(id=pk)
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        bio_info = request.POST['bio_info']
        email = request.POST['email']
        avatar = request.FILES.get('avatar')

        obj.first_name = first_name
        obj.last_name = last_name
        obj.bio_info = bio_info
        obj.email = email
        if avatar is not None:
            obj.avatar = avatar
        obj.save()

        messages.success(request, 'Profile updated successfully!')

    return redirect('profiles:myProfile')



class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/listProfile.html'
    context_object_name = 'profiles'  
    # or object_list

    def get_queryset(self):
        otherProfile = Profile.objects.all().exclude(user=self.request.user)
        return otherProfile
    

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/otherProfile.html'

    def get_object(self,**kwargs):
        pk = self.kwargs.get('pk')
        view_profile = Profile.objects.get(pk=pk)
        return view_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()
        my_profile = Profile.objects.get(user=self.request.user)
        if view_profile.user in my_profile.friends.all():
            friends=True
        else:
            friends=False
        context["friends"] = friends
        try:
            status_ = get_object_or_404(Relationship, sender= view_profile.pk)
            if (status_.status == 'send'):
                print("eta db ma send vayo")
                context["pending"] = True

            print("xiro")

        except:
            print("eta db ma send gako chaina")

        return context
    

def unfriend_profile(request):
    if request.method == "POST":
        my_profile = Profile.objects.get(user=request.user)
        pk = request.POST['profile_pk']
        obj = Profile.objects.get(pk=pk)

        if obj.user in my_profile.friends.all():
            my_profile.friends.remove(obj.user)
            obj.friends.remove(my_profile.user)

        # else:
        #     my_profile.friends.add(obj.user)

        return redirect(request.META.get('HTTP_REFERER'))
        # return redirect('profiles:profile-detail-view', obj.pk)

    return redirect('profiles:profile-list-view')


def invites_received_view(request):
    myprofile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(myprofile)

    print(qs.exists())
    context = {
        'qs':qs,
        'request_exist':qs.exists()
    }

    return render(request, 'profiles/my_invites.html', context)


def send_request(request):
    if request.method =='POST':
        receiver_pk = request.POST['profile_pk']
        sender_pk = request.user.profile.pk

        receiver_ = Profile.objects.get(pk= receiver_pk)
        sender_ = Profile.objects.get(pk= sender_pk)
        # print(sender_)
        # print(receiver_)

        notify, created= Relationship.objects.get_or_create(sender=sender_, receiver=receiver_, status="send")
        # print(notify.status)
        # print(created)

        return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect('profiles:profile-list-view')


def accept_friend_request(request,pk):
    # friends_status = Relationship.objects.get_or_create(pk=pk, )
    friend_request = get_object_or_404(Relationship, pk=pk)
    friend_request.status = 'accepted'
    friend_request.save()
    # return HttpResponse("Request")
    return redirect(request.META.get('HTTP_REFERER'))


def reject_friend_request(request,pk):
    # friends_status = Relationship.objects.get_or_create(pk=pk, )
    friend_request = get_object_or_404(Relationship, pk=pk)
    friend_request.status = 'rejected'
    friend_request.save()
    # return HttpResponse("reject vayo")
    return redirect(request.META.get('HTTP_REFERER'))