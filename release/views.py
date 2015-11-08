from django.shortcuts import render, redirect
from .models import Release
from datetime import date, timedelta
from calendar import monthrange

PLAN_STATUSES = [Release.NEW, Release.IN_PROGRESS, Release.READY]
HISTORY_STATUSES = [Release.CANCELED, Release.FAILED, Release.SUCCESSFUL]
PLAN = 'plan'
HISTORY = 'history'

MONTH = 'month'
WEEK = 'week'
DAYS = { MONTH: 28, WEEK: 7 }
DEFAULT_MAX_RELEASE_FOR_DAY = 7

def period(request, status, period, year, month, day):
    if period == MONTH:
        number_of_days = monthrange(int(year), int(month))[1]
        start = date(int(year), int(month), 1)
    else:
        number_of_days = DAYS[WEEK]
        start = date(int(year), int(month), int(day))
        start = start - timedelta(start.weekday())

    if status == PLAN:
        statuses = PLAN_STATUSES
    else:
        statuses = HISTORY_STATUSES

    end = start + timedelta(number_of_days)
    releases = Release.objects.filter(start_time__range=(start, end)).filter(status__in=statuses).order_by('start_time')

    days = {}
    for delta in range(0, number_of_days):
        d = start + timedelta(delta)
        days[d] = []

    for release in releases:
        days[release.start_time.date()].append(release)
    max_releases_per_day = max(map(lambda x: len(x), days.values()))
    if period == MONTH and max_releases_per_day < DEFAULT_MAX_RELEASE_FOR_DAY:
        max_releases_per_day = DEFAULT_MAX_RELEASE_FOR_DAY

    if period == MONTH:
        start = date(int(year), int(month), 15)

    return render(request, period + '.html', context={
        'day': day,
        'month': month,
        'year': year,
        'releases': days,
        'days': sorted(days.keys()),
        'max_releases_range': range(0, max_releases_per_day),
        'prev_period': start - timedelta(number_of_days),
        'next_period': start + timedelta(number_of_days),
        'status': status,
        'period': period,
        'statuses': [PLAN, HISTORY],
        'periods': [WEEK, MONTH]
    })

def index(request):
    d = date.today()
    return redirect('plan/week/' + str(d.year) + '/' + str(d.month) + '/' + str(d.day))

