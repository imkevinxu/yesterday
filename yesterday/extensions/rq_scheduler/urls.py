from django.conf.urls import url

from .views import jobs, job_detail, delete_job, enqueue_job, clear_jobs, actions

urlpatterns = [
    url(r'^$', jobs, name='jobs'),
    url(r'^jobs/actions/$', actions, name='actions'),
    url(r'^jobs/clear/$', clear_jobs, name='clear_jobs'),
    url(r'^jobs/(?P<job_id>[-\w]+)/$', job_detail, name='job_detail'),
    url(r'^jobs/(?P<job_id>[-\w]+)/delete/$', delete_job, name='delete_job'),
    url(r'^jobs/(?P<job_id>[-\w]+)/enqueue/$', enqueue_job, name='enqueue_job'),
]
