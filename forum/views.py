from django.shortcuts import render, get_object_or_404
from .models import Topic, User, Post
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    topics = Topic.objects.order_by('-published_date')
    context = {
        'topics' : topics
    }
    return render(request, 'forum/index.html', context)


def login_template(request):
    return render(request, 'forum/login.html', {})


def savepost(request):
    post_data = request.POST['post_text']
    topic_id = request.POST['topic_id']
    if 'post_id' in request.POST:
        post_id = request.POST['post_id']
    else:
        post_id = None
    post = Post(text=post_data, author=request.user, topic_id=topic_id, parent_id=post_id)
    post.save()
    return HttpResponseRedirect(reverse('forum:index'))

def edit_post(request):
    post_data = request.POST['edit_text']
    post_id = request.POST['post_id']
    post = get_object_or_404(Post, pk=post_id)
    post.text = post_data
    post.save()
    return HttpResponseRedirect(reverse('forum:index'))

def delete_post(request):
    post_id = request.POST["post_id"]
    post = get_object_or_404(Post, pk=post_id)
    post.text = "This comment has been deleted by its author."
    post.save()
    return HttpResponseRedirect(reverse('forum:index'))

def register_user(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    next = request.POST['next']

    if password != confirm_password:
        return HttpResponseRedirect(reverse('forum:index'))

    user = User.objects.create_user(username, email, password)
    login(request, user)

    if next == '':
        return HttpResponseRedirect(reverse('forum:index'))
    return HttpResponseRedirect(next)

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    next = request.POST['next']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if next == '':
            return HttpResponseRedirect(reverse('forum:index'))
        return HttpResponseRedirect(next)
    return HttpResponseRedirect(reverse('forum:index'))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('forum:index'))


def post_to_html(post, depth):
    r = '\t'*depth + post.text + '\n'
    for child in post.children.order_by('date'):
        r += post_to_html(child, depth+1)
    return r

def test_recursion(request):
    output = '<pre>'
    topics = Topic.objects.order_by('published_date')
    for topic in topics:
        output += topic.title + '\n'
        posts = topic.posts.filter(parent__isnull=True)
        for post in posts:
            output += post_to_html(post, 1)
    return HttpResponse(output + '</pre>')