from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from datetime import date, timedelta
import json

from models import Entry


def _build_entries(user, start, end):
    entries = list(user.entry_set.filter(date__range=(start, end)))
    curr = start
    day = timedelta(days=1)
    for entry in entries:
        # Fill all missing dates up to the entry
        while curr < entry.date:
            yield Entry(user=user, date=curr, count=0)
            curr += day
        # Return the entry
        yield entry
        curr += day
    # Fill all missing dates until the end
    while curr <= end:
        yield Entry(user=user, date=curr, count=0)
        curr += day


def _get_entries(user):
    end = date.today()
    start = end - timedelta(days=30)
    return list(_build_entries(user, start, end))


def track_view(request):
    entries = _get_entries(request.user)
    return render(request, 'track.html', locals())


@csrf_exempt
def entries_view(request, id=None):
    data = json.load(request)
    if data['id']:
        entry = Entry.objects.get(id=data['id'], user=request.user)
        entry.count = data['count']
        entry.save()
    else:
        Entry.objects.create(user=request.user, date=data['date'][:10], count=data['count'])
    return JsonResponse({})
