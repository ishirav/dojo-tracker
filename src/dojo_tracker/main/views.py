from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse
from django.conf import settings

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


def personal_view(request, token):
    user = authenticate(username=token, password=settings.DEFAULT_USER_PASSWORD)
    # TODO when user is None
    login(request, user)
    return HttpResponseRedirect(reverse('track'))
