from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse

from .models import Board

def index(request):
   return render(request, 'board/index.html')

# def detail(request, board_id):
#     board = Board.objects.get(id=board_id)
#     return render(request, 'board/detail.html', {'board': board})

def write(request):
    return render(request, 'board/write.html')

# def write_board(request):
#     b = Board(title=request.POST['title'], content=request.POST['detail'], author="choi", pub_date=timezone.now())
#     b.save()
#     return HttpResponseRedirect(reverse('board:index'))

# def create_reply(request, board_id):
#     b = Board.objects.get(id = board_id)
#     b.reply_set.create(comment=request.POST['comment'], rep_date=timezone.now())
#     return HttpResponseRedirect(reverse('board:detail', args=(board_id,)))   