import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import date, timedelta
from news.models import Post, Subscribe

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives # send_mail
from NewsPaper.settings import ALLOWED_HOSTS

logger = logging.getLogger(__name__)



def my_job():

    some_day_last_week = date.today() - timedelta(days=7)
    posts = Post.objects.filter(created__date__gte=some_day_last_week)

    for post in posts:
        for cat in post.cats.all():
            for sub in Subscribe.objects.filter(category_id=cat.id):



                if sub.user.email:


                    html_content = render_to_string(
                        'post/pochta_week.html', {
                            'user': sub.user,
                            'title': post.title,
                            'cat': cat,
                            'text': post.text[:50],
                            'link': f'http://{ALLOWED_HOSTS[0]}:8000/news/{post.id}',
                        }
                    )


                    msg = EmailMultiAlternatives(
                        subject=f'{cat} создана {post.created.strftime("%d-%m-%Y %H:%M")}',
                        from_email='Skill.testing@yandex.ru',
                        to=[sub.user.email],
                    )
                    msg.attach_alternative(html_content, "text/html")
                    try:
                        msg.send()
                    except Exception as e:
                        print('Not sen email')



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

                day_of_week="mon", hour="02", minute="00"
            ),

            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="01", minute="00"
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