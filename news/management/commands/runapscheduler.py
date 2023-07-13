import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from news.models import Category, Post
from datetime import datetime, timedelta
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


def my_job():
    #  Your job processing logic here...

    week = (datetime.now() - timedelta(days=7)).date()

    for i in Category.objects.all():
        if i.subscribers.all():
            subs = [j for j in i.subscribers.all()]
            news = Post.objects.filter(categories=i.id, time_create__gt=week)

            html_content = render_to_string(
                'week.html',
                {
                    'news': news,
                }
            )

            subject = "Посты за неделю из ваших подписок"

            msg = EmailMultiAlternatives(
                subject=subject,
                from_email='iamrock@yandex.ru',
                to=[i.email for i in subs],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"  # every week
            ),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")