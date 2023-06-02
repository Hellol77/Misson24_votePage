from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages

# 로그인 확인
def login_message_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "로그인한 사용자만 이용할 수 있습니다.")
            return redirect(settings.LOGIN_URL)
        return function(request, *args, **kwargs)
    return wrap