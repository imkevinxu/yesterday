from django.conf.urls import url

from .views import jobs, job_detail, queues, clear_queue, delete_job, requeue_job_view, actions

urlpatterns = [
    url(r'^$', queues, name='rq_home'),
    url(r'^queues/(?P<queue_index>[\d]+)/$', jobs, name='rq_jobs'),
    url(r'^queues/(?P<queue_index>[\d]+)/empty/$', clear_queue, name='rq_clear'),
    url(r'^queues/(?P<queue_index>[\d]+)/(?P<job_id>[-\w]+)/$', job_detail, name='rq_job_detail'),
    url(r'^queues/(?P<queue_index>[\d]+)/(?P<job_id>[-\w]+)/delete/$', delete_job, name='rq_delete_job'),
    url(r'^queues/(?P<queue_index>[\d]+)/(?P<job_id>[-\w]+)/requeue/$', requeue_job_view, name='rq_requeue_job'),
    url(r'^queues/actions/(?P<queue_index>[\d]+)/$', actions, name='rq_actions'),
]
