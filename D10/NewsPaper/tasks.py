from celery import shared_task
import time

from news.models import Post, Subscribe
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives # send_mail
from NewsPaper.settings import ALLOWED_HOSTS
from datetime import date, timedelta, datetime

@shared_task
def hello():
    time.sleep(1)
    print("Hello, world!")
    print(f"Date: {datetime.now()}")

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)

@shared_task
def post_mail_week():

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

@shared_task
def mail_new_post(id):
    post = Post.objects.get(pk=id)
    for cat in post.cats.all():
        for sub in Subscribe.objects.filter(category_id=cat.id):



            if sub.user.email:




                html_content = render_to_string(
                    'post/pochta.html', {
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

