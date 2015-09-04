from django.shortcuts import render,  redirect, HttpResponse
from .models import Release, DeploymentFact, Artifact, Environment
from datetime import date, timedelta, datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

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
        number_of_days = DAYS[MONTH]
    else:
        number_of_days = DAYS[WEEK]

    if status == PLAN:
        statuses = PLAN_STATUSES
    else:
        statuses = HISTORY_STATUSES

    start = date(int(year), int(month), int(day))
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


def fact_list(request):

    result = DeploymentFact.objects
    if request.method == 'POST':
        body = request.POST
        host = body['host']
        artifact = body['artifact']
        version = body['version']
        get_date = body['date']
        page = 1
    else:
        host = request.GET.get('host')
        artifact = request.GET.get('artifact')
        version = request.GET.get('version')
        get_date = request.GET.get('date')
        page = request.GET.get('page')

    if get_date:
        buf_date = datetime.strptime(get_date, '%Y-%m-%d')
        buf_date = (get_date, (buf_date + timedelta(1)))
    else:
        buf_date = 0

    if host and artifact and version and buf_date:
        result = result.filter(host=host).filter(artifact__type__name=artifact).filter(
            artifact__version=version).filter(datetime__range=buf_date)
    elif host and artifact:
        if version:
            result = result.filter(host=host).filter(artifact__type__name=artifact).filter(
                artifact__version=version).order_by('-datetime')
        elif buf_date:
            result = result.filter(host=host).filter(artifact__type__name=artifact).filter(
                datetime__range=buf_date).order_by('-datetime')
        else:
            result = result.filter(host=host).filter(artifact__type__name=artifact).order_by('-datetime')
    elif version and buf_date:
        if host:
            result = result.filter(host=host).filter(artifact__version=version).filter(
                datetime__range=buf_date).order_by('-datetime')
        elif artifact:
            result = result.filter(artifact__type__name=artifact).filter(
                artifact__version=version).filter(datetime__range=buf_date).order_by('-datetime')
        else:
            result = result.filter(host=host).filter(artifact__type__name=artifact).filter(
                artifact__version=version).filter(datetime__range=buf_date).order_by('-datetime')
    elif host:
        if version:
            result = result.filter(host=host).filter(artifact__version=version).order_by('-datetime')
        elif buf_date:
            result = result.filter(host=host).filter(datetime__range=buf_date).order_by('-datetime')
        else:
            result = result.filter(host=host).order_by('-datetime')
    elif artifact:
        if version:
            result = result.filter(artifact__type__name=artifact).filter(artifact__version=version).order_by('-datetime')
        elif buf_date:
            result = result.filter(artifact__type__name=artifact).filter(datetime__range=buf_date).order_by('-datetime')
        else:
            result = result.filter(artifact__type__name=artifact).order_by('-datetime')
    elif version:
            result = result.filter(artifact__version=version).order_by('-datetime')
    elif buf_date:
            result = result.filter(datetime__range=buf_date).order_by('-datetime')
    else:
        result = result.all().order_by('-datetime')

    if result:
        result2 = ''
    else:
        result2 = 'Nothing Found'

    paginator = Paginator(result, 50)
    try:
        pagin_result = paginator.page(page)
    except PageNotAnInteger:
        pagin_result = paginator.page(1)
    except EmptyPage:
        pagin_result = paginator.page(paginator.num_pages)
    return render(request, 'fact.html', context={
        'result': pagin_result,
        'result2': result2,
        'host': host,
        'artifact': artifact,
        'version': version,
        'date': get_date
    })


@csrf_exempt
def fact_create(request):
    body = json.loads(request.body.decode('utf-8'))
    try:
        artifact = Artifact.objects.filter(type__name=body['artifact']).filter(version=body['version'])[0]
        resp1 = ''
    except:
        artifact = ''
        resp1 = 'artifact not found '
    try:
        environment = Environment.objects.get(name=body['environment'])
        resp2 = ''
    except:
        environment = ''
        resp2 = 'environment not found '

    if body['status'] == 'FL' or body['status'] == 'SC':
        print(body['status'])
        status = body['status']
        resp3 = ''
    else:
        print(body['status'])
        status = ''
        resp3 = 'status incorrect'

    if artifact and environment and status:
        fact = DeploymentFact.objects.create(status=status,
                                             host=body['host'],
                                             artifact=artifact,
                                             environment=environment)
        fact.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(resp1 + resp2 + resp3)


def fact_request(request):
    return render(request, 'factrequest.html')
