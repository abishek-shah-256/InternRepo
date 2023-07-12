from django.shortcuts import render,redirect, HttpResponse
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import Profile


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
        return context
    

def friend_unfriend_profile(request):
    if request.method == "POST":
        my_profile = Profile.objects.get(user=request.user)
        pk = request.POST['profile_pk']
        obj = Profile.objects.get(pk=pk)

        if obj.user in my_profile.friends.all():
            my_profile.friends.remove(obj.user)

        else:
            my_profile.friends.add(obj.user)

        return redirect(request.META.get('HTTP_REFERER'))
        # return redirect('profiles:profile-detail-view', obj.pk)

    
    return redirect('profiles:profile-list-view')