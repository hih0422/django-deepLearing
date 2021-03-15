from django.shortcuts import render

# Create your views here.
def deep_runing(request):
    return render(request, 'deep_running.html', {})