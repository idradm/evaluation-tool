import json
from django.http import HttpResponse
from django.shortcuts import render
from hlidskjalf.models import Run, ResultItem, Type, Result, DataItem


# Create your views here.
def index(request):
    runs = Run.objects.all()
    return render(request, 'main.html', {'runs': runs})


def details(request, id):
    # render stats
    run = Run.objects.get(id=id)
    results = ResultItem.objects.filter(run=run)
    template = "%s.html" % results[0].item.item.real_type if results else ''

    total = len(DataItem.objects.filter(set=run.set))
    found = len(results)
    types = {}

    for result in results:
        if result.result is not None:
            if result.result.type is not None:
                if result.result.type.name not in types:
                    types[result.result.type.name] = 0
                types[result.result.type.name] += 1

    type_coverages = {}
    for type, value in types.items():
        type_coverages[type] = [
            value,
            round((float(value) / float(found)) * 100, 2)
        ]

    stats = {
        'total': total,
        'found': found,
        'coverage': round((float(found) / float(total)) * 100, 2),
        'types': type_coverages
    }

    buttons = Type.objects.all()
    return render(request, 'run.html', {'template': template, 'results': results, 'buttons': buttons, 'stats': stats})


def save(request, id, value):
    result = Result.objects.get(id=id)
    result.type = Type.objects.get(id=value)
    result.save()

    return HttpResponse(json.dumps(int(value)), content_type="application/json")