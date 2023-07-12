from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import login,authenticate,logout
from .forms import CreateUserForm
from django.contrib.auth.forms import AuthenticationForm
from app1.models import CustomUser, Post, Comment
from profiles.models import Profile
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt




def home(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        status_content = request.POST['status_content']
        image1 = request.FILES.get('postImage')

        if status_content == "" and image1 is not None:
            post = Post.objects.create(author=request.user.profile,post_img=image1)
            # post = Post.objects.create(author=profile.id,post_img=image1)
            message = "Image Posted successfully"
            return HttpResponse(message)

        elif status_content !="" and image1 is None:
            post = Post.objects.create(author=request.user.profile,content=status_content)
            message = "status message Posted successfully"
            return HttpResponse(message)

        elif status_content !="" and image1 is not None:
            post = Post.objects.create(author=request.user.profile,content=status_content,post_img=image1)
            message = "both Posted successfully"
            return HttpResponse(message)
        
        else:
            message = "Post unsuccessfull"
            return HttpResponse(message)
        
    # print("yaaa dekhiiiiiiiiiiiiiii")
    profile_friends = Profile.objects.get(pk=request.user.pk)
    profile_friends = [user for user in profile_friends.get_friends()]
    post_data = Post.objects.filter(author__user = request.user).union(Post.objects.filter(author__user__id__in=[friend_id.id for friend_id in profile_friends]))
    # print(result)
        

    # post_data = Post.objects.all()
    post_comment_list = []
    for p in post_data:
        comments = Comment.objects.filter(comment_post=p)
        post_dict_with_comments ={
            'id':p.id,
            'profile_avatar': p.author.avatar.url,
            'content': p.content,
            'user_firstname': p.author.first_name,
            'user_lastname': p.author.last_name,
            'user_email': p.author.email,
            'post_img':p.post_img.url if p.post_img else None,
            'created_at':p.created_at.strftime('%d %B, %Y' ', %H:%M'),
            # 'comment':[comment.comment_content for comment in comments],
            # 'commented_user_img':[comment.commented_user.avatar.url for comment in comments],
            # 'user_comment': {
            #     'content':[comment.comment_content for comment in comments],
            #     'commented_user_img': [comment.commented_user.avatar.url for comment in comments]

            # },

            'comments': zip([comment.comment_content for comment in comments], [comment.commented_user.avatar.url for comment in comments])


        }
        post_comment_list.append(post_dict_with_comments)
        # print(post_comment_list)

    context = {
        'posts' :post_data,
        'profile': profile,
        'post_comment_list':post_comment_list
    }
    return render(request, 'app1/home.html',context)

def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful" )
            return redirect('signin')
            # gender = form.cleaned_data.get('gender')
        else:
            messages.error(request, "Registration unsuccessfull. Invalid information")
            print("valid vayena")

    return render(request, 'app1/signUp.html')

def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        if email == "" or password == "":
            messages.error(request, 'Email or passwor dcannot be empty')

        else:
            user = CustomUser.objects.filter(email=email).exists()
            if user:
                user_obj = CustomUser.objects.get(email=email)
                print('yooooooo')
                # print(user_obj.friends)
                correct_pw = user_obj.check_password(password)
                if correct_pw:
                    login(request, user_obj)
                    return redirect('home')
                else:
                    messages.error(request, 'Password incorrect')
                    
            else:
                messages.info(request, 'Invalid email')

    return render(request, 'app1/signIn.html')
    
def logout(request):
    logout(request)
    return redirect('signin')

def getupdatedPost(request):
    # post_data = Post.objects.all().values()
    profile = Profile.objects.get(user=request.user)
    post_data = Post.objects.all()
    post_list = []
    
    for p in post_data:
        comments = Comment.objects.filter(comment_post=p)

        post_dict = {
            'id':p.id,
            'profile_avatar': p.author.avatar.url,
            'content': p.content,
            'user_firstname': p.author.first_name,
            'user_lastname': p.author.last_name,
            'user_email': p.author.email,
            'post_img':p.post_img.url if p.post_img else None,
            'created_at':p.created_at.strftime('%d %B, %Y' ', %H:%M'),
            'comments':[comment.comment_content for comment in comments],
            # 'comments': zip([comment.comment_content for comment in comments], [comment.commented_user.avatar.url for comment in comments]),
            'commented_user':  [comment.commented_user.avatar.url for comment in comments],
            'loggedin_user_Profile': profile.avatar.url,
        }


        post_list.append(post_dict)

    # return JsonResponse(list(post_data), safe = False)
    return JsonResponse(post_list, safe = False)

@csrf_protect
def handleComment(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        comment = request.POST['comment']

        if comment != '':
            profile = Profile.objects.filter(user=request.user)
            # print(profile[0].slug)
            pos = Post.objects.get(id = post_id)
            cmnt = Comment.objects.create(comment_post=pos,commented_user=request.user.profile,comment_content=comment)

    # for displaying the data in the home html
    profile = Profile.objects.get(user=request.user)
    post_data = Post.objects.all()
    post_comment_list = []
    for p in post_data:
        comments = Comment.objects.filter(comment_post=p)
        post_dict_with_comments ={
            'id':p.id,
            'profile_avatar': p.author.avatar.url,
            'content': p.content,
            'user_firstname': p.author.first_name,
            'user_lastname': p.author.last_name,
            'user_email': p.author.email,
            'post_img':p.post_img.url if p.post_img else None,
            'created_at':p.created_at.strftime('%d %B, %Y' ', %H:%M'),
            'comment':[comment.comment_content for comment in comments],
            'commented_user':  [comment.commented_user.avatar.url for comment in comments],


        }
        post_comment_list.append(post_dict_with_comments)
    
    context = {
        'posts' :post_data,
        'profile': profile,
        'post_comment_list':post_comment_list
    }
    
    return redirect('home')



def userprofile(request):
    return render(request, 'app1/userprofile.html')
    
def userpost(request):
    pass

def messenger(request):
    return render(request, 'app1/messenger.html')

