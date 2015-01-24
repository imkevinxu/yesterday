from django.core.mail import send_mail

from django_rq import enqueue, job


@job
def send_mail_job(subject, message, from_email, recipient_list,
                  fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None):
    """
    `send_mail` function as django_rq job

    Usage: send_mail_job.delay(args)
    """
    send_mail(subject, message, from_email, recipient_list,
              fail_silently, auth_user, auth_password, connection, html_message)


def enqueue_send_mail(subject, message, from_email, recipient_list,
                      fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None):
    """
    `send_mail` function automatically enqueued

    Usage: enqueue_send_mail(args)
    """
    enqueue(send_mail, subject, message, from_email, recipient_list,
            fail_silently, auth_user, auth_password, connection, html_message)
