from django.db import models
from django.conf import settings
from jobs.models import Job


class Application(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    cv = models.FileField(upload_to='cvs/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')  # يمنع التقديم مرتين

    def __str__(self):
        return f"{self.user.email} - {self.job.title}"