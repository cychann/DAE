from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import HttpResponse
import json
from django.db.models import Q

# Create your views here.
def main(request):
    posts = Post.objects.all()

    paginator = Paginator(posts, 12)
    page = request.GET.get('page')
    all_posts = paginator.get_page(page)

    close_soon_posts = Post.objects.all().order_by('meet_date')

    paginator2 = Paginator(close_soon_posts, 8)
    soon_page = request.GET.get('page')
    soon_posts = paginator2.get_page(soon_page)

    return render(request, 'main.html', {'allPost':all_posts, 'soon_post': soon_posts})


def category(request, category):
    posts = Post.objects.filter(category = category)
    paginator = Paginator(posts, 12)
    page = request.GET.get('page')
    all_posts = paginator.get_page(page)
    return render(request, 'party.html', {'allPost':all_posts}) #templates 파일명 추후 수정하기


def detail(request, id):
    post = get_object_or_404(Post, pk = id)
    cat_name = transCategory(post.category)
    loc_name = transLocation(post.location)

    comments = Comment.objects.filter(post_id=id, comment_id__isnull=True)

    re_comments = []
    for comment in comments:
        re_comments += list(Comment.objects.filter(comment_id=comment.id))

    form = CommentForm()
    return render(request, 'party_detail.html', {'post':post, 'comments':comments, 're_comments':re_comments, 'form': form, 'category_name':cat_name, 'location_name':loc_name})


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
    print("1")
    if request.is_ajax():
        post_id = request.GET.get('post_id') #post_id!! 이름 주의
        post = Post.objects.get(id=post_id)
    print("2")
    user = request.user
    if post.like.filter(id = user.id).exists():
        post.like.remove(user)
        message = "좋아요 취소"
    else:
        post.like.add(user)
        message = "좋아요"
        print("3")
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


def transCategory(code):
    category_trans = {
        'c01': '스포츠', 
        'c02': '게임', 
        'c03': '독서', 
        'c04': '함께 결제', 
        'c05': '언어', 
        'c06': '공예', 
        'c07': '음악', 
        'c08': '문화',
        'c09': '공모전',
    }
    name = category_trans[code]
    return name


def transLocation(code):
    location_trans = {
        'l01': '서울', 
        'l02': '경기', 
        'l03': '강원', 
        'l04': '충남', 
        'l05': '충북', 
        'l06': '경남',
        'l07': '경북',
        'l08': '전남', 
        'l09': '전북',
        'l10': '인천', 
        'l11': '대전', 
        'l12': '광주', 
        'l13': '대구',
        'l10': '울산', 
        'l11': '부산', 
        'l03': '제주',
    }
    name = location_trans[code]
    return name


#신청하기
def applyParty(request, post_id):
    post = Post.objects.get(id=post_id)

    user = request.user
    if post.apply.filter(id = user.id).exists(): #이미 신청했다면 신청 취소
        post.apply.remove(user)
    else: #신청하기
        post.apply.add(user)

    post.CurrentCount = post.apply.count() 
    post.save()
    return redirect('party:detail', post_id) 


#currentCount 추가하는 메소드
# def plusCurrentCount(id):
#     post = get_object_or_404(Post, pk = id)
#     post.currentCount += 1
#     post.save()

# def subCurrentCount(id):
#     post = get_object_or_404(Post, pk = id)
#     post.currentCount -= 1
#     post.save()
