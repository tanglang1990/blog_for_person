from django.shortcuts import render, redirect

from users.forms import RegisteForm


def register(request):
    if request.method == "POST":
        form = RegisteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = RegisteForm()
    return render(request, 'users/base_form.html', {'title': '注册', 'form': form})


def success(request):
    return render(request, 'users/success.html', {'title': '操作成功'})