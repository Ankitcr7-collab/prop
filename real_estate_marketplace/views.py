from django.http import HttpResponse, JsonResponse
from listings.models import Properties



def home(request):
    data = Properties.objects.prefetch_related('user')
    print(data)
    return HttpResponse('Home Page')