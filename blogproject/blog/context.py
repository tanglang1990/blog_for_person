from django.conf import settings


def title(request):
    return {'TITLE': settings.TITLE}
