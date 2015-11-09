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

    def month_inc(year, month):
        if month < 12:
            return_date = date(year, month + 1, 1)
        else:
            return_date = date(year + 1, 1, 1)
        return return_date

    def month_reduce(year, month):
        if month == 1:
            return_date = date(year - 1, 12, 1)
        else:
            return_date = date(year, month - 1, 1)
        return return_date

    iyear = int(year)
    imonth = int(month)
    iday = int(day)

    if period == MONTH:
        number_of_days = monthrange(iyear, imonth)[1]
        start = date(iyear, imonth, 1)
        prev_period = month_reduce(iyear, imonth)
        next_period = month_inc(iyear, imonth)
    else:
        number_of_days = DAYS[WEEK]
        day_of_month = date(iyear, imonth, iday)
        day_of_week = timedelta(day_of_month.weekday())
        start = day_of_month - day_of_week
        prev_period = start - timedelta(number_of_days)
        next_period = start + timedelta(number_of_days)

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

    return render(request, period + '.html', context={
        'day': day,
        'month': month,
        'year': year,
        'releases': days,
        'days': sorted(days.keys()),
        'max_releases_range': range(0, max_releases_per_day),
        'prev_period': prev_period,
        'next_period': next_period,
        'status': status,
        'period': period,
        'statuses': [PLAN, HISTORY],
        'periods': [WEEK, MONTH]
    })

def index(request):
    d = date.today()
    return redirect('plan/week/' + str(d.year) + '/' + str(d.month) + '/' + str(d.day))

