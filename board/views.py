from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import HttpResponse
import json
from django.db.models import Q

# def index(request):
#    return render(request, 'board/index.html')

# # def detail(request, board_id):
# #     board = Board.objects.get(id=board_id)
# #     return render(request, 'board/detail.html', {'board': board})

# def write(request):
#     return render(request, 'board/write.html')

# def write_board(request):
#     b = Board(title=request.POST['title'], content=request.POST['detail'], author="choi", pub_date=timezone.now())
#     b.save()
#     return HttpResponseRedirect(reverse('board:index'))

# def create_reply(request, board_id):
#     b = Board.objects.get(id = board_id)
#     b.reply_set.create(comment=request.POST['comment'], rep_date=timezone.now())
#     return HttpResponseRedirect(reverse('board:detail', args=(board_id,)))   

def main(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 12)
    page = request.GET.get('page')
    all_posts = paginator.get_page(page)

    return render(request, 'main.html', {'allPost':all_posts})

def category(request, category):
    posts = Post.objects.filter(category = category)
    paginator = Paginator(posts, 12)
    page = request.GET.get('page')
    all_posts = paginator.get_page(page)
    return render(request, 'category.html', {'allPost':all_posts}) #templates 파일명 추후 수정하기


def detail(request, id):
    post = get_object_or_404(Post, pk = id)
    comments = Comment.objects.filter(post_id=id, comment_id__isnull=True)

    re_comments = []
    for comment in comments:
        re_comments += list(Comment.objects.filter(comment_id=comment.id))

    form = CommentForm()
    return render(request, 'party_detail.html', {'post':post, 'comments':comments, 're_comments':re_comments, 'form': form})


def create_comment(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = Post.objects.get(pk=post_id)
            comment.writer = request.user
            comment.save()
    return redirect('/detail/' + str(post_id))


def create_re_comment(request, post_id, comment_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = Post.objects.get(pk=post_id)
            comment.comment_id = Comment.objects.get(pk=comment_id)
            comment.writer = request.user
            comment.save()
    return redirect('/detail/' + str(post_id))


def new(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.upload_date = timezone.now() 
            new_post.author = request.user
            new_post.save()
            return redirect('party:detail', new_post.id) #수정해야할수도..
        return redirect('party:main')
    else:
        post_form = PostForm()
        return render(request, 'party_create.html', {'form':post_form})


def edit(request, id):
    post = get_object_or_404(Post, pk = id)
    if request.method == 'GET':
        post_form = PostForm(instance = post)
        return render(request, 'party_update.html', {'edit_post' : post_form, 'post' : post})
    else:
        post_form = PostForm(request.POST, request.FILES, instance = post)
        if post_form.is_valid():
            edit_post = post_form.save(commit=False)
            edit_post.save()
        return redirect('party:detail', edit_post.id) 


def delete(request, id):
    delete_post = Post.objects.get(id = id)
    if request.user == delete_post.author:
        delete_post.delete()
    return redirect('party:main')


def post_likes(request):
    if request.is_ajax():
        post_id = request.GET.get('post_id') #post_id!! 이름 주의
        post = Post.objects.get(id=post_id)

    user = request.user
    if post.like.filter(id = user.id).exists():
        post.like.remove(user)
        message = "좋아요 취소"
    else:
        post.like.add(user)
        message = "좋아요"
    context = {
        'like_count' : post.like.count(),
        'message' : message,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")


def search(request):
    keyword = request.GET.get('keyword')
    search_list = Post.objects.filter(Q(body__icontains=keyword)|Q(title__icontains=keyword)).distinct()
    
    paginator = Paginator(search_list, 12)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'search.html', {'posts':posts})