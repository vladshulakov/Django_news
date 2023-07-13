from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import PostCategory

@receiver(m2m_changed, sender=PostCategory)
def notify_subs(sender, instance, action, **kwargs):
    if 'post_add' in action:
        subject = f'Новая запись в категории, на которую вы подписаны'
        subs=[i.subscribers.all() for i in instance.categories.all()]
        send_mail(
            subject=subject,
            message=f'''{instance.title}
{instance.post_text[:20]}...''',
            from_email='iamrock@yandex.ru',
            recipient_list=[j.email for i in subs for j in i]
        )