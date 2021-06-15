from users.models import User
from datetime import datetime


class SetLastVisitMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            user.last_login = datetime.now()
            user.save()
        response = self.get_response(request)
        return response
