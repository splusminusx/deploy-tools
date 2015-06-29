from django.shortcuts import render, redirect
from .models import Release
from datetime import date, timedelta


def week(request, year, month, day):
    start = date(int(year), int(month), int(day))
    end = start + timedelta(7)
    releases = Release.objects.filter(start_time__range=(start, end)).order_by('start_time')
    days = {}
    for delta in range(0, 7):
        day = start + timedelta(delta)
        days[day] = []
    for release in releases:
        days[release.start_time.date()].append(release)
    max_releases_per_day = max(map(lambda x: len(x), days.values()))
    return render(request, 'week.html', context={
        'releases': days,
        'days': sorted(days.keys()),
        'max_releases_range': range(0, max_releases_per_day)
    })


def index(request):
    d = date.today()
    return redirect('week/' + str(d.year) + '/' + str(d.month) + '/' + str(d.day))
