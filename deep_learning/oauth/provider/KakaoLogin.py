import os,json,requests

from django.shortcuts import redirect

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))   # 프로젝트 root 경로
with open(os.path.join(BASE_DIR, 'conf\secret.json'), 'rb') as secret_file:
    secrets = json.load(secret_file)

class KakaoLogin:

    def get_code(self):
        app_rest_api_key = secrets['KAKAO']['REST_API_KEY']
        redirect_uri = secrets['KAKAO']['MAIN_DOMAIN'] + "/kakao/callback"
        return app_rest_api_key, redirect_uri

    def get_token(self,request):
        app_rest_api_key = secrets['KAKAO']["REST_API_KEY"]
        redirect_uri = secrets['KAKAO']['MAIN_DOMAIN'] + "/kakao/callback"
        code = request.GET.get('code')

        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={code}"
        )

        token_response_json = token_request.json()

        error = token_response_json.get('error', None)

        # 에러 발생시
        if error is not None:
            raise KakaoException()
        access_token = token_response_json.get("access_token")

        return access_token

    def get_profile(self,access_token):
        profile_request = requests.post(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        id = profile_json.get("id")
        email = kakao_account.get("email", None)
        if email is None:
            raise KakaoException()
        profile = kakao_account.get("profile")
        nickname = profile.get("nickname")

        return id, email, nickname


class KakaoException(Exception):
    pass
