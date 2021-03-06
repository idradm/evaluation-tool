import json
from django.http import HttpResponse
from django.shortcuts import render
from hlidskjalf.models import Run, ResultItem, Type, Result
from hlidskjalf.stats import Stats
from hlidskjalf.matcher import EpisodesMatcher


# Create your views here.
def index(request, page):
    if page is None:
        runs = Run.objects.all().order_by('-id')[:5]
    else:
        s, e = 5 * int(page), (5 * int(page)) + 5
        runs = Run.objects.all().order_by('-id')[s:e]
    result = []
    for run in runs:
        run.stats = Stats.get(run)
        result.append(run)
    return render(request, 'main.html', {'runs': result})


def details(request, id, page):
    # render stats
    run = Run.objects.get(id=id)
    results = ResultItem.objects.filter(run=run)

    if page is not None:
        s, e = 20 * int(page), (20 * int(page)) + 20
        results = results[s:e]
    else:
        to_check = []
        matcher = EpisodesMatcher()
        for result in results.filter(result__type__isnull=True):
            if not matcher.match(result):
                to_check.append(result)
        results = to_check

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
    return render(request, 'done.html', {})


def test(request, id):
    run = Run.objects.get(id=id)
    results = ResultItem.objects.filter(run=run)
    matcher = EpisodesMatcher()
    print(matcher.match(results[0]))
    return HttpResponse(json.dumps(int(1)), content_type="application/json")