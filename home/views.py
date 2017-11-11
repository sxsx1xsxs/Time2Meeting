from django.shortcuts import render


def guidance(request):
    return render(request, 'home/guidance.html')


def team(request):
    return render(request, 'home/team.html')