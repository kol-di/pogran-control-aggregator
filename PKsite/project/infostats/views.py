from django.shortcuts import render
from django.http import HttpResponse


from PKdb.db_locations import MongodbService


def index(request):
    db = MongodbService.get_instance()
    data = db.get_data()
    return HttpResponse(data)
    # return HttpResponse("Hello, world. You're at the infostats index.")
