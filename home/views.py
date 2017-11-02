from django.shortcuts import render

# Create your views here.
def homepage(request):
    user_email = request.COOKIES.get('email')
    if not user_email:
        return render(request, 'home/homepage.html')
    else:
        return render(request, 'home/homepage.html')

def guidance(request):
    return render(request, 'home/guidance.html')

def team(request):
    return render(request, 'home/team.html')