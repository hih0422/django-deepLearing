from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login
from deep_learning.oauth.provider.KakaoLogin import KakaoLogin
from django.shortcuts import redirect

kakao_login_auth = KakaoLogin()

# Create your views here.
def deep_learning(request):
    return render(request, 'main.html', {})

# def login(request):
#     return render(request, 'auth/login.html', {})

# #csrf 미사용 선언
# @method_decorator(csrf_exempt, name='dispatch')
def kakao_login(request):
    app_rest_api_key, redirect_uri = kakao_login_auth.get_code()
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )

def kakao_callback(request):
    access_token = kakao_login_auth.get_token(request)

    id, email, nickname = kakao_login_auth.get_profile(access_token)

    user, created = User.objects.get_or_create(
        email=email,
        username=nickname
    )
    if created:
        user.set_password(None)
    user.name = nickname
    user.is_active = True
    user.save()

    login(request, user, 'deep_learning.oauth.KakaoBackend')
    kakao_login_auth.set_session(id,access_token)

    return redirect(
        f'http://127.0.0.1:8000/'
    )
