from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import PostCategory
from news.tasks import new_post

@receiver(m2m_changed, sender=PostCategory)
def notify_subs(sender, instance, action, **kwargs):
    if 'post_add' in action:
        new_post.apply_async([instance.id], countdown=5)