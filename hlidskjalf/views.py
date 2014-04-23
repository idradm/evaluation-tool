import json
from django.http import HttpResponse
from django.shortcuts import render
from hlidskjalf.models import Run, ResultItem, Type, Result


# Create your views here.
def index(request):
    runs = Run.objects.all()
    print(runs)
    return render(request, 'main.html', {'runs': runs})


def details(request, id):
    run = Run.objects.get(id=id)
    results = ResultItem.objects.filter(run=run)
    buttons = Type.objects.all()
    return render(request, 'run.html', {'results': results, 'buttons': buttons})


def save(request, id, value):
    result = Result.objects.get(id=id)
    result.type = Type.objects.get(id=value)
    result.save()

    return HttpResponse(json.dumps(int(value)), content_type="application/json")