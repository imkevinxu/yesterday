from django.test import TestCase
from django.core import mail
from django.conf import settings

from ..mail import send_mail_job, enqueue_send_mail


class CoreEmailUtilsTestCase(TestCase):
    def setUp(self):
        self.subject = "[Test] CoreEmailUtilsTestCase"
        self.message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean lobortis ornare vestibulum. Sed euismod euismod mattis. Suspendisse potenti. Vestibulum eget faucibus lacus. Quisque in eros augue. Sed diam lorem, finibus congue auctor vel, volutpat a lacus. Proin ut pellentesque nisi, ut dignissim erat. Donec fringilla venenatis est, a tempor turpis tempus a. Praesent eu magna lectus."
        self.from_email = "Testbot <test@%s>" % settings.PROJECT_DOMAIN
        self.recipient_list = ["test@example.com"]

    def test_send_mail_job(self):
        self.assertEqual(len(mail.outbox), 0)
        send_mail_job.delay(self.subject, self.message, self.from_email, self.recipient_list)
        self.assertEqual(len(mail.outbox), 1)

        testEmail = mail.outbox[0]
        self.assertIn("CoreEmailUtilsTestCase", testEmail.subject)
        self.assertIn("Lorem ipsum", testEmail.body)
        self.assertIn("Testbot", testEmail.from_email)
        self.assertIn("test@example.com", testEmail.to)

    def test_enqueue_send_mail(self):
        self.assertEqual(len(mail.outbox), 0)
        enqueue_send_mail(self.subject, self.message, self.from_email, self.recipient_list)
        self.assertEqual(len(mail.outbox), 1)

        testEmail = mail.outbox[0]
        self.assertIn("CoreEmailUtilsTestCase", testEmail.subject)
        self.assertIn("Lorem ipsum", testEmail.body)
        self.assertIn("Testbot", testEmail.from_email)
        self.assertIn("test@example.com", testEmail.to)
