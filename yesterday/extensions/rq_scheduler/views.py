from __future__ import division

from django.contrib import admin
from django_rq.settings import SHOW_ADMIN_LINK

# Change default admin template to include Redis links
if SHOW_ADMIN_LINK:
    admin.site.index_template = 'rq_scheduler/templates/index.html'

from math import ceil

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.timezone import make_aware, utc

from rq.job import Job
from rq.exceptions import NoSuchJobError

from django_rq import get_scheduler


# Heavily modified views originally from
# https://github.com/ui/django-rq/blob/master/django_rq/views.py
@staff_member_required
def jobs(request):
    scheduler = get_scheduler()
    jobs_list = scheduler.get_jobs(with_times=True)
    items_per_page = 100
    num_jobs = len(jobs_list)
    page = int(request.GET.get('page', 1))

    if num_jobs > 0:
        last_page = int(ceil(num_jobs / items_per_page))
        page_range = range(1, last_page + 1)
        offset = items_per_page * (page - 1)

        jobs_list = jobs_list[offset:offset + items_per_page]
        for job, scheduled_at in jobs_list:
            job.scheduled_at = make_aware(scheduled_at, utc)
            job.created_at = make_aware(job.created_at, utc)
        jobs = [job for job, scheduled_time in jobs_list]
    else:
        jobs = []
        page_range = []

    context_data = {
        'title': 'Scheduled Jobs',
        'jobs': jobs,
        'num_jobs': num_jobs,
        'page': page,
        'page_range': page_range,
    }
    return render(request, 'rq_scheduler/templates/jobs.html', context_data)


@staff_member_required
def job_detail(request, job_id):
    scheduler = get_scheduler()
    try:
        job = Job.fetch(job_id, connection=scheduler.connection)
    except NoSuchJobError:
        raise Http404("Couldn't find job with this ID: %s" % job_id)

    if job in scheduler:
        jobs_list_with_times = scheduler.get_jobs(with_times=True)
        jobs_list = [j for j, scheduled_at in jobs_list_with_times]
        job.scheduled_at = jobs_list_with_times[jobs_list.index(job)][1]
        job.scheduled_at = make_aware(job.scheduled_at, utc)

    job.created_at = make_aware(job.created_at, utc)
    job.enqueued_at = make_aware(job.enqueued_at, utc) if job.enqueued_at else None

    context_data = {
        'title': 'Job Info',
        'job': job,
    }
    return render(request, 'rq_scheduler/templates/job_detail.html', context_data)


@staff_member_required
def delete_job(request, job_id):
    scheduler = get_scheduler()
    job = Job.fetch(job_id, connection=scheduler.connection)

    if request.method == 'POST':
        job.cancel()
        messages.info(request, 'You have successfully deleted %s' % job.id)
        return redirect('rq_scheduler:jobs')

    context_data = {
        'title': 'Are you sure?',
        'job': job,
    }
    return render(request, 'rq_scheduler/templates/delete_job.html', context_data)


@staff_member_required
def enqueue_job(request, job_id):
    scheduler = get_scheduler()
    job = Job.fetch(job_id, connection=scheduler.connection)

    if request.method == 'POST':
        scheduler.enqueue_job(job)
        messages.info(request, 'You have successfully enqueued %s' % job.id)
        return redirect('rq_scheduler:jobs')

    context_data = {
        'title': 'Are you sure?',
        'job': job,
    }
    return render(request, 'rq_scheduler/templates/enqueue_job.html', context_data)


@staff_member_required
def clear_jobs(request):
    scheduler = get_scheduler()
    if request.method == 'POST':
        for job in scheduler.get_jobs():
            job.cancel()
        messages.info(request, 'You have successfully cleared all scheduled jobs')
        return redirect('rq_scheduler:jobs')

    context_data = {
        'title': 'Are you sure?',
    }
    return render(request, 'rq_scheduler/templates/clear_jobs.html', context_data)


@staff_member_required
def actions(request):
    scheduler = get_scheduler()

    if request.method == 'POST' and request.POST.get('action', False):
        # Confirmation page for selected Action
        if request.POST.get('_selected_action', False):
            context_data = {
                'action': request.POST['action'],
                'job_ids': request.POST.getlist('_selected_action'),
            }
            return render(request, 'rq_scheduler/templates/confirm_action.html', context_data)

        # Performing the actual action
        elif request.POST.get('job_ids', False):
            job_ids = request.POST.getlist('job_ids')

            if request.POST['action'] == 'delete':
                for job_id in job_ids:
                    job = Job.fetch(job_id, connection=scheduler.connection)
                    job.cancel()
                messages.info(request, 'You have successfully deleted %s jobs!' % len(job_ids))
            elif request.POST['action'] == 'enqueue':
                for job_id in job_ids:
                    job = Job.fetch(job_id, connection=scheduler.connection)
                    scheduler.enqueue_job(job)
                messages.info(request, 'You have successfully enqueued %d  jobs!' % len(job_ids))

    return redirect('rq_scheduler:jobs')
