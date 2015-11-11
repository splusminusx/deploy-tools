from django.shortcuts import render,  redirect, HttpResponse
from .models import Release, DeploymentFact, Artifact, Environment
from datetime import date, timedelta, datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
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

    _date = date(int(year), int(month), int(day))
    if period == MONTH:
        number_of_days = monthrange(_date.year, _date.month)[1]
        start = date(_date.year, _date.month, 1)
        prev_period = month_reduce(_date.year, _date.month)
        next_period = month_inc(_date.year, _date.month)
    else:
        number_of_days = DAYS[WEEK]
        day_of_week = timedelta(_date.weekday())
        start = _date - day_of_week
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


def fact_list(request):

    if request.method == 'POST':
        body = request.POST
        page = 1
    else:
        body = request.GET
        page = body['page']

    host = body['host']
    artifact = body['artifact']
    version = body['version']

    if body['date']:
        buf_date = (body['date'], (datetime.strptime(body['date'], '%Y-%m-%d') + timedelta(1)))
    else:
        buf_date = 0

    result = create_db_request(host, artifact, version, buf_date)

    if result:
        message = ''
    else:
        message = 'Nothing Found'

    paginator = Paginator(result, 100)
    try:
        pagin_result = paginator.page(page)
    except PageNotAnInteger:
        pagin_result = paginator.page(1)
    except EmptyPage:
        pagin_result = paginator.page(paginator.num_pages)
    return render(request, 'fact.html', context={
        'result': pagin_result,
        'message': message,
        'host': host,
        'artifact': artifact,
        'version': version,
        'date': body['date']
    })


def create_db_request(host, artifact, version, buf_date):
    fact = DeploymentFact.objects
    if not (host and artifact and version and buf_date):
        fact = fact.all()
    if host:
        fact = fact.filter(host=host)
    if artifact:
        fact = fact.filter(artifact__type__name=artifact)
    if version:
        fact = fact.filter(artifact__version=version)
    if buf_date:
        fact = fact.filter(datetime__range=buf_date)

    return fact


@csrf_exempt
def fact_create(request):
    body = json.loads(request.body.decode('utf-8'))
    error_response = ''
    try:
        artifact = Artifact.objects.filter(type__name=body['artifact']).filter(version=body['version'])[0]
        error_response += ''
    except:
        artifact = ''
        error_response += 'artifact not found \n'
    try:
        environment = Environment.objects.get(name=body['environment'])
        error_response += ''
    except:
        environment = ''
        error_response += 'environment not found \n'

    if body['status'] == 'FL' or body['status'] == 'SC':
        print(body['status'])
        status = body['status']
        error_response += ''
    else:
        print(body['status'])
        status = ''
        error_response += 'status incorrect \n'

    if artifact and environment and status:
        fact = DeploymentFact.objects.create(status=status,
                                             host=body['host'],
                                             artifact=artifact,
                                             environment=environment)
        fact.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(error_response)


def fact_show(request):
    return render(request, 'factshow.html')
