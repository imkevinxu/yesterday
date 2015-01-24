from django.test import TestCase
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from django_rq import get_scheduler

from accounts.factories import AdminUserFactory

from datetime import datetime
from pytz import timezone


class RQSchedulerViewExtensionsTestCase(TestCase):
    def setUp(self):
        """ Create a superuser and log in """
        self.user = AdminUserFactory(email='test@example.com')
        self.client.login(email='test@example.com', password='password')

        self.subject = "[Test] RQSchedulerViewExtensionsTestCase"
        self.message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean lobortis ornare vestibulum. Sed euismod euismod mattis. Suspendisse potenti. Vestibulum eget faucibus lacus. Quisque in eros augue. Sed diam lorem, finibus congue auctor vel, volutpat a lacus. Proin ut pellentesque nisi, ut dignissim erat. Donec fringilla venenatis est, a tempor turpis tempus a. Praesent eu magna lectus."
        self.from_email = "Testbot <test@%s>" % settings.PROJECT_DOMAIN
        self.recipient_list = ["test@example.com"]

        self.scheduler = get_scheduler()
        self.western = timezone('America/Los_Angeles')
        self.scheduled_time = self.western.localize(datetime(2020, 1, 1))
        self.scheduler.enqueue_at(self.scheduled_time, send_mail, self.subject, self.message, self.from_email, self.recipient_list)

    def tearDown(self):
        for job in self.scheduler.get_jobs():
            job.cancel()

    def test_jobs_view_extension(self):
        response = self.client.get(reverse('rq_scheduler:jobs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rq_scheduler/templates/jobs.html')
        self.assertContains(response, "Jan. 1, 2020, midnight")

    def test_job_detail_view_extension(self):
        job_id = self.scheduler.get_jobs()[0].id
        response = self.client.get(reverse('rq_scheduler:job_detail', kwargs={'job_id': job_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rq_scheduler/templates/job_detail.html')
        self.assertContains(response, "Jan. 1, 2020, midnight")
        self.assertContains(response, "Not queued yet")

        response = self.client.get(reverse('rq_scheduler:job_detail', kwargs={'job_id': "fake"}))
        self.assertEqual(response.status_code, 404)

    def test_delete_job_view_extension(self):
        job_id = self.scheduler.get_jobs()[0].id
        response = self.client.get(reverse('rq_scheduler:delete_job', kwargs={'job_id': job_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rq_scheduler/templates/delete_job.html')
        self.assertContains(response, job_id)
        self.assertEqual(len(self.scheduler.get_jobs()), 1)

        response = self.client.post(reverse('rq_scheduler:delete_job', kwargs={'job_id': job_id}))
        self.assertRedirects(response, reverse('rq_scheduler:jobs'))
        self.assertEqual(len(self.scheduler.get_jobs()), 0)

    def test_enqueue_job_view_extension(self):
        job_id = self.scheduler.get_jobs()[0].id
        response = self.client.get(reverse('rq_scheduler:enqueue_job', kwargs={'job_id': job_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rq_scheduler/templates/enqueue_job.html')
        self.assertContains(response, job_id)
        self.assertEqual(len(self.scheduler.get_jobs()), 1)

        response = self.client.post(reverse('rq_scheduler:enqueue_job', kwargs={'job_id': job_id}))
        self.assertRedirects(response, reverse('rq_scheduler:jobs'))
        self.assertEqual(len(self.scheduler.get_jobs()), 0)

        response = self.client.get(reverse('rq_scheduler:job_detail', kwargs={'job_id': job_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rq_scheduler/templates/job_detail.html')
        self.assertContains(response, "django.core.mail.send_mail")

    def test_clear_jobs_view_extension(self):
        for i in range(2):
            self.scheduler.enqueue_at(self.scheduled_time, send_mail, self.subject, self.message, self.from_email, self.recipient_list)

        response = self.client.get(reverse('rq_scheduler:clear_jobs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rq_scheduler/templates/clear_jobs.html')
        self.assertEqual(len(self.scheduler.get_jobs()), 3)

        response = self.client.post(reverse('rq_scheduler:clear_jobs'))
        self.assertRedirects(response, reverse('rq_scheduler:jobs'))
        self.assertEqual(len(self.scheduler.get_jobs()), 0)

    def test_action_view_extension(self):
        response = self.client.get(reverse('rq_scheduler:actions'))
        self.assertRedirects(response, reverse('rq_scheduler:jobs'))

    def test_action_delete_view_extension(self):
        for i in range(2):
            self.scheduler.enqueue_at(self.scheduled_time, send_mail, self.subject, self.message, self.from_email, self.recipient_list)

        job_ids = [job.id for job in self.scheduler.get_jobs()]
        delete_action_payload = {'action': 'delete', '_selected_action': job_ids}
        response = self.client.post(reverse('rq_scheduler:actions'), delete_action_payload)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rq_scheduler/templates/confirm_action.html')
        self.assertContains(response, job_ids[0])
        self.assertEqual(len(self.scheduler.get_jobs()), 3)

        delete_action_payload = {'action': 'delete', 'job_ids': job_ids}
        response = self.client.post(reverse('rq_scheduler:actions'), delete_action_payload)
        self.assertRedirects(response, reverse('rq_scheduler:jobs'))
        self.assertEqual(len(self.scheduler.get_jobs()), 0)

    def test_action_enqueue_view_extension(self):
        for i in range(2):
            self.scheduler.enqueue_at(self.scheduled_time, send_mail, self.subject, self.message, self.from_email, self.recipient_list)

        job_ids = [job.id for job in self.scheduler.get_jobs()]
        enqueue_action_payload = {'action': 'enqueue', '_selected_action': job_ids}
        response = self.client.post(reverse('rq_scheduler:actions'), enqueue_action_payload)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rq_scheduler/templates/confirm_action.html')
        self.assertContains(response, job_ids[0])
        self.assertEqual(len(self.scheduler.get_jobs()), 3)

        enqueue_action_payload = {'action': 'enqueue', 'job_ids': job_ids}
        response = self.client.post(reverse('rq_scheduler:actions'), enqueue_action_payload)
        self.assertRedirects(response, reverse('rq_scheduler:jobs'))
        self.assertEqual(len(self.scheduler.get_jobs()), 0)
