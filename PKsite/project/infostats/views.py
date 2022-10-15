from django.shortcuts import render

from .dash_apps import timeline, piechart, dynamics


def index(request):
    return render(request, "index.html", {})


def info_timeline(request):
    return render(request, "info_timeline.html", {})


def info_piechart(request):
    return render(request, "info_piechart.html", {})


def info_dynamics(request):
    return render(request, "info_dynamics.html", {})


def stories(request):
    return render(request, "stories.html", {})
