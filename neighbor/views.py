from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    try:
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')
        current_user=request.user
        profile =Profile.objects.get(username=current_user)
    except ObjectDoesNotExist:
        return redirect('create-profile')
    return render(request,'index.html')
@login_required(login_url='/accounts/login/')
def my_profile(request):
    current_user=request.user
    profile =Profile.objects.get(username=current_user)
    return render(request,'profile/user_profile.html',{"profile":profile})


@login_required(login_url='/accounts/login/')
def user_profile(request,username):
    user = User.objects.get(username=username)
    profile =Profile.objects.get(username=user)
    
@login_required(login_url='/accounts/login/')
def create_profile(request):
    current_user=request.user
    if request.method=="POST":
        form =ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.username = current_user
            profile.save()
        return redirect('/')
    else:
        form = ProfileForm()
        return render(request,'profile/profile_form.html',{"form":form})
@login_required(login_url='/accounts/login/')
def update_profile(request):
    current_user=request.user
    if request.method=="POST":
        instance = Profile.objects.get(username=current_user)
        form =ProfileForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.username = current_user
            profile.save()

        return redirect('Index')

    elif Profile.objects.get(username=current_user):
        profile = Profile.objects.get(username=current_user)
        form = ProfileForm(instance=profile)
    else:
        form = ProfileForm()

    return render(request,'profile/update_profile.html',{"form":form})

@login_required(login_url='/accounts/login/')
def blog(request):
    current_user=request.user
    profile=Profile.objects.get(username=current_user)
    blogposts = BlogPost.objects.filter(neighbourhood=profile.neighbourhood)

    return render(request,'blogs.html',{"blogposts":blogposts})

@login_required(login_url='/accounts/login/')
def view_blog(request,id):
    current_user = request.user

    try:
        comments = Comment.objects.filter(post_id=id)
    except:
        comments =[]

    blog = BlogPost.objects.get(id=id)
    if request.method =='POST':
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.username = current_user
            comment.post = blog
            comment.save()
    else:
        form = CommentForm()

    return render(request,'read.html',{"blog":blog,"form":form,"comments":comments})

