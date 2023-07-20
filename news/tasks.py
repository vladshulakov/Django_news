from celery import shared_task
from news.models import Post, Category
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from datetime import datetime, timedelta


@shared_task
def new_post(instance_id):

    instance = Post.objects.get(id=instance_id)

    html_content = render_to_string(
        'new_post.html',
        {
            'post': instance,
        }
    )

    subject = f'Новая запись в категории, на которую вы подписаны'

    subs = [i.subscribers.all() for i in instance.categories.all()]
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email='iamrock@yandex.ru',
        to=[j.email for i in subs for j in i],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task
def weekly_newsletter():

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
