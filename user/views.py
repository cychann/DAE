from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
def user_delete(request):
    if request.method == 'POST': #POST로 요청 오면 회원탈퇴(정말로 탈퇴하시겠습니까? >> 확인)
        request.user.delete()
        return redirect('party:main')
    return render(request, 'user_delete.html') #[정말로 탈퇴하시겠습니까?] 페이지로 이동