import json
from django.http import HttpResponse
from django.shortcuts import render
from hlidskjalf.models import Run, ResultItem, Type, Result
from hlidskjalf.stats import Stats


# Create your views here.
def index(request):
    runs = Run.objects.all()
    result = []
    for run in runs:
        run.stats = Stats.get(run)
        result.append(run)
    return render(request, 'main.html', {'runs': result})


def details(request, id):
    # render stats
    run = Run.objects.get(id=id)
    results = ResultItem.objects.filter(run=run)
    template = "%s.html" % results[0].item.item.real_type if results else ''

    buttons = Type.objects.all()
    return render(request, 'run.html', {'template': template, 'results': results, 'buttons': buttons, 'stats': Stats.get(run)})


def save(request, id, value):
    result = Result.objects.get(id=id)
    result.type = Type.objects.get(id=value)
    result.save()

    return HttpResponse(json.dumps(int(value)), content_type="application/json")


def calculate(request, id):
    run = Run.objects.get(id=id)
    Stats.calculate(run)
    return HttpResponse(json.dumps("done"), content_type="application/json")