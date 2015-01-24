from django.test import TestCase
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template.defaultfilters import date, time

from django_rq import get_queue

from accounts.factories import AdminUserFactory

from datetime import datetime


class DjangoRQExtensionsTestCase(TestCase):
    def setUp(self):
        """ Create a superuser and log in """
        self.user = AdminUserFactory(email='test@example.com')
        self.client.login(email='test@example.com', password='password')

        self.subject = "[Test] DjangoRQExtensionsTestCase"
        self.message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean lobortis ornare vestibulum. Sed euismod euismod mattis. Suspendisse potenti. Vestibulum eget faucibus lacus. Quisque in eros augue. Sed diam lorem, finibus congue auctor vel, volutpat a lacus. Proin ut pellentesque nisi, ut dignissim erat. Donec fringilla venenatis est, a tempor turpis tempus a. Praesent eu magna lectus."
        self.from_email = "Testbot <test@%s>" % settings.PROJECT_DOMAIN
        self.recipient_list = ["test@example.com"]

        self.queue = get_queue(async=True)
        for i in range(3):
            self.queue.enqueue(send_mail, self.subject, self.message, self.from_email, self.recipient_list)

    def tearDown(self):
        self.queue.empty()

    def test_jobs_view_extension(self):
        response = self.client.get(reverse('rq_jobs', kwargs={'queue_index': 0}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'django_rq/templates/jobs.html')
        self.assertContains(response, "%s, %s" % (date(datetime.now()), time(datetime.now())))

        self.queue.empty()
        response = self.client.get(reverse('rq_jobs', kwargs={'queue_index': 0}))
        self.assertEqual(response.status_code, 200)

    def test_job_detail_view_extension(self):
        job_id = self.queue.get_jobs()[0].id
        response = self.client.get(reverse('rq_job_detail', kwargs={'queue_index': 0, 'job_id': job_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'django_rq/templates/job_detail.html')
        self.assertContains(response, "%s, %s" % (date(datetime.now()), time(datetime.now())))

        response = self.client.get(reverse('rq_job_detail', kwargs={'queue_index': 0, 'job_id': "fake"}))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('rq_job_detail', kwargs={'queue_index': 0, 'job_id': "empty"}))
        self.assertEqual(response.status_code, 200)

    def test_queues_view_extension(self):
        response = self.client.get(reverse('rq_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'django_rq/stats.html')

    def test_clear_queue_view_extension(self):
        response = self.client.get(reverse('rq_clear', kwargs={'queue_index': 0}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'django_rq/clear_queue.html')

        response = self.client.post(reverse('rq_clear', kwargs={'queue_index': 0}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('rq_jobs', kwargs={'queue_index': 0}))

    def test_delete_job_view_extension(self):
        job_id = self.queue.get_jobs()[0].id
        response = self.client.get(reverse('rq_delete_job', kwargs={'queue_index': 0, 'job_id': job_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'django_rq/delete_job.html')

        response = self.client.post(reverse('rq_delete_job', kwargs={'queue_index': 0, 'job_id': job_id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('rq_jobs', kwargs={'queue_index': 0}))

    def test_requeue_job_view_extension(self):
        job_id = self.queue.get_jobs()[0].id

        response = self.client.get(reverse('rq_requeue_job', kwargs={'queue_index': 0, 'job_id': job_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'django_rq/delete_job.html')

        response = self.client.post(reverse('rq_requeue_job', kwargs={'queue_index': 0, 'job_id': job_id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('rq_jobs', kwargs={'queue_index': 0}))

    def test_action_view_extensions(self):
        response = self.client.get(reverse('rq_actions', kwargs={'queue_index': 0}))
        self.assertRedirects(response, reverse('rq_jobs', kwargs={'queue_index': 0}))

    def test_action_delete_view_extension(self):
        job_ids = [job.id for job in self.queue.get_jobs()]
        delete_action_payload = {'action': 'delete', '_selected_action': job_ids}
        response = self.client.post(reverse('rq_actions', kwargs={'queue_index': 0}), delete_action_payload)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'django_rq/confirm_action.html')
        self.assertContains(response, job_ids[0])

        delete_action_payload = {'action': 'delete', 'job_ids': job_ids}
        response = self.client.post(reverse('rq_actions', kwargs={'queue_index': 0}), delete_action_payload)
        self.assertRedirects(response, reverse('rq_jobs', kwargs={'queue_index': 0}))
