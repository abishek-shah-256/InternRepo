import uuid
from django.utils import timezone

def get_random_code():
    code = str(uuid.uuid4())[:8].replace('-','').lower()
    return code


class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.user.is_authenticated:
                request.user.profile.last_online = timezone.now()
                request.user.profile.save()

        except:
            print("Profile does not exists")


        response = self.get_response(request)
        return response