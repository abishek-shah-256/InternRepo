from django.conf import settings
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.contrib.auth.forms import AuthenticationForm
from app1.models import CustomUser, Post, Comment
from profiles.models import Profile
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import random, string
from datetime import datetime, timedelta
import base64
import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
import requests

# -----for email verification of registered user------------------
def generate_token(length=64):
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(length))
    return token

def send_mail(url,email):
    to_valid_email = email
    email_from = 'developabishek@gmail.com'
    password = 'rikuquugypfpwoci'
    email_to = 'developabishek@gmail.com'

    # email_string = 'This is a test email sent by Python.'
    message = MIMEMultipart("alternative")
    html = f"""\
            <html>
            <body>
                <p>Hi,<br>
                How are you?<br>
                <a href="{url}">Click me!</a> 
                 For Registration 
                </p>
            </body>
            </html>
            """
    
    part2 = MIMEText(html, "html")
    message.attach(part2)
   
    context = ssl.create_default_context() 
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(email_from, password)
            server.sendmail(email_from, email_to, message.as_string())
    except Exception as e:
        print(e)

def check_user_existence(user_id):
    try:
        user = CustomUser.objects.get(id = user_id) 
        return user
    except CustomUser.DoesNotExist:
        return None

def authenticatee(request,token=None):
    # print("decoded datatatataaaa")
    # print(token)

    if token != None:
        decoded_data = base64.b64decode(token).decode('utf-8')
        data = json.loads(decoded_data)
        token_user_id = data['user_id']
        # print(data['user_id'])      

        user = check_user_existence(token_user_id)

        
        if user is not None:
            print("verifired xaaaaaaaaaaaaaaaa")
            print(user.email)
            user.is_verified = True
            user.save()
        else:
            print("verifired xaaaaaaaaaaiiiiiiiinnnnnnnaaaaaa")
            request.user.is_verified = False
            request.user.save()

        return redirect('signin')
    else:

        return HttpResponse("Token Aayena !")
# -----for email verification of registered user endss--------------------




@login_required(login_url='signin')
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
            user = form.save(commit=False)
            user.first_name = user.first_name.lower()
            user.last_name = user.last_name.lower()
            user.save()
            # login(request, user)
            messages.success(request, "Please check your email to complete the Registration process" )
            # -----------for email verification------
            token = generate_token()
            access_token ={
                'user_id':user.id,
                'user_firstname': user.first_name,
                'user_lastname': user.last_name
            }
            json_data = json.dumps(access_token)
            encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
            domain = request.build_absolute_uri('/')
            url = domain +  f'authenticate/{encoded_data}/' 
            email = form.cleaned_data.get('email')
            send_mail(url,email)
            # -----------for email verification ends----------


            return redirect('signin')
            # gender = form.cleaned_data.get('gender')
        else:
            messages.error(request, "Registration unsuccessfull. Invalid information in the form")
            print("valid vayena")

    return render(request, 'app1/signUp.html')


def signin(request):
    secret_key = settings.RECAPTCHA_SECRET_KEY
    if request.user.is_authenticated:
        return redirect('home')
    else:

        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            # ---for recaptcha version3----------------------
            recaptcha_token = request.POST['g-recaptcha-response']
            data ={
                'response': recaptcha_token,
                'secret': secret_key
            }
            resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result_json = resp.json()
            print(result_json)

            if not result_json.get('success'):
                return render(request, 'app1/signIn.html', {'is_robot': True})
            # ---for recaptcha version3 ends----------------------

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

                        if user_obj.is_verified == True:
                            login(request, user_obj)
                            return redirect('home')
                        
                        elif user_obj.is_verified == False:
                            return HttpResponse("Please check your mail to complete Registration")
                    
                    else:
                        messages.error(request, 'Password incorrect')
                        
                else:
                    messages.info(request, 'Invalid email')

    return render(request, 'app1/signIn.html')
    

def logoutt(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
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


@login_required(login_url='signin')
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


@login_required(login_url='signin')
def userprofile(request):
    return render(request, 'app1/userprofile.html')

@login_required(login_url='signin')
def userpost(request):
    pass

@login_required(login_url='signin')
def messenger(request):
    return render(request, 'app1/messenger.html')

