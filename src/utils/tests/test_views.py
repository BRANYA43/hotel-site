from django.http import HttpResponse


def imitating_view(request):
    return HttpResponse(request)
