from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.conf import settings

from TestAlice.WebInterfaceApp.forms import LoginForm
from TestAlice.WebInterfaceApp.models import UserRequest


@login_required
def get_history(request):
    query_results = UserRequest.objects.order_by('request_datetime').all()
    template = loader.get_template('request_table.html')
    context = {
        'query_results': query_results,
    }
    return HttpResponse(template.render(context, request))


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    redirect_url = request.GET.get('next')
                    if redirect_url:
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Login failed')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
