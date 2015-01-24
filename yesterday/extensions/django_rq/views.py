# Subclassing Django RQ views
# https://github.com/ui/django-rq/blob/master/django_rq/views.py

from __future__ import division

from math import ceil

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.timezone import make_aware, utc

from redis.exceptions import ResponseError
from rq import requeue_job, Worker
from rq.job import Job
from rq.exceptions import NoSuchJobError, InvalidJobOperationError

from django_rq.queues import get_connection, get_queue_by_index
from django_rq.settings import QUEUES_LIST


# Extended `jobs` and `job_detail` view functions in order to make datetime timezone-aware
@staff_member_required
def jobs(request, queue_index):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)

    items_per_page = 100
    num_jobs = queue.count
    page = int(request.GET.get('page', 1))

    if num_jobs > 0:
        last_page = int(ceil(num_jobs / items_per_page))
        page_range = range(1, last_page + 1)
        offset = items_per_page * (page - 1)
        jobs = queue.get_jobs(offset, items_per_page)
        for job in jobs:
            job.created_at = make_aware(job.created_at, utc)
            job.enqueued_at = make_aware(job.enqueued_at, utc)
    else:
        jobs = []
        page_range = []

    context_data = {
        'title': 'Jobs in %s' % queue.name,
        'queue': queue,
        'queue_index': queue_index,
        'jobs': jobs,
        'num_jobs': num_jobs,
        'page': page,
        'page_range': page_range,
    }
    return render(request, 'django_rq/templates/jobs.html', context_data)


@staff_member_required
def job_detail(request, queue_index, job_id):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)
    try:
        job = Job.fetch(job_id, connection=queue.connection)
        job.created_at = make_aware(job.created_at, utc)
        job.enqueued_at = make_aware(job.enqueued_at, utc)
    except NoSuchJobError:
        raise Http404("Couldn't find job with this ID: %s" % job_id)

    context_data = {
        'title': 'Job Info',
        'queue_index': queue_index,
        'job': job,
        'queue': queue,
    }
    return render(request, 'django_rq/templates/job_detail.html', context_data)


# Extended django_rq view functions with added 'title' context
@staff_member_required
def queues(request):
    queues = []
    for index, config in enumerate(QUEUES_LIST):
        queue = get_queue_by_index(index)
        queue_data = {
            'name': queue.name,
            'jobs': queue.count,
            'index': index,
        }
        if queue.name == 'failed':
            queue_data['workers'] = '-'
        else:
            connection = get_connection(queue.name)
            all_workers = Worker.all(connection=connection)
            queue_workers = [worker for worker in all_workers if queue in worker.queues]
            queue_data['workers'] = len(queue_workers)
        queues.append(queue_data)

    context_data = {
        'title': 'RQ Queues',
        'queues': queues
    }
    return render(request, 'django_rq/stats.html', context_data)


@staff_member_required
def clear_queue(request, queue_index):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)

    if request.method == 'POST':
        try:
            queue.empty()
            messages.info(request, 'You have successfully cleared the queue %s' % queue.name)
        except ResponseError as e:  # pragma: no cover
            if 'EVALSHA' in e.message:
                messages.error(request, 'This action is not supported on Redis versions < 2.6.0, please use the bulk delete command instead')
            else:
                raise e
        return redirect('rq_jobs', queue_index)

    context_data = {
        'title': 'Are you sure?',
        'queue_index': queue_index,
        'queue': queue,
    }
    return render(request, 'django_rq/clear_queue.html', context_data)


@staff_member_required
def delete_job(request, queue_index, job_id):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)
    job = Job.fetch(job_id, connection=queue.connection)

    if request.method == 'POST':
        # Remove job id from queue and delete the actual job
        queue.connection._lrem(queue.key, 0, job.id)
        job.delete()
        messages.info(request, 'You have successfully deleted %s' % job.id)
        return redirect('rq_jobs', queue_index)

    context_data = {
        'title': 'Are you sure?',
        'queue_index': queue_index,
        'job': job,
        'queue': queue,
    }
    return render(request, 'django_rq/delete_job.html', context_data)


@staff_member_required
def requeue_job_view(request, queue_index, job_id):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)
    job = Job.fetch(job_id, connection=queue.connection)

    if request.method == 'POST':
        try:  # pragma: no cover
            requeue_job(job_id, connection=queue.connection)
            messages.info(request, 'You have successfully requeued %s' % job.id)
            return redirect('rq_job_detail', queue_index, job_id)
        except InvalidJobOperationError as e:
            messages.error(request, e.message)
            return redirect('rq_jobs', queue_index)

    context_data = {
        'title': 'Are you sure?',
        'queue_index': queue_index,
        'job': job,
        'queue': queue,
    }
    return render(request, 'django_rq/delete_job.html', context_data)


@staff_member_required
def actions(request, queue_index):
    queue_index = int(queue_index)
    queue = get_queue_by_index(queue_index)

    if request.method == 'POST' and request.POST.get('action', False):
        # Confirmation page for selected Action
        if request.POST.get('_selected_action', False):
            context_data = {
                'title': 'Are you sure?',
                'queue_index': queue_index,
                'action': request.POST['action'],
                'job_ids': request.POST.getlist('_selected_action'),
                'queue': queue,
            }
            return render(request, 'django_rq/confirm_action.html', context_data)

        # Performing the actual action
        elif request.POST.get('job_ids', False):
            job_ids = request.POST.getlist('job_ids')

            if request.POST['action'] == 'delete':
                for job_id in job_ids:
                    job = Job.fetch(job_id, connection=queue.connection)
                    # Remove job id from queue and delete the actual job
                    queue.connection._lrem(queue.key, 0, job.id)
                    job.delete()
                messages.info(request, 'You have successfully deleted %s jobs!' % len(job_ids))
            elif request.POST['action'] == 'requeue':  # pragma: no cover
                for job_id in job_ids:
                    requeue_job(job_id, connection=queue.connection)
                messages.info(request, 'You have successfully requeued %d  jobs!' % len(job_ids))

    return redirect('rq_jobs', queue_index)
