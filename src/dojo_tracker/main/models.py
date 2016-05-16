from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Entry(models.Model):

    user = models.ForeignKey(User)
    date = models.DateField()
    count = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['user', 'date']
        unique_together = ['user', 'date']
        verbose_name_plural = 'entries'

    def __unicode__(self):
        return '%s / %s' % (self.user.get_full_name() or self.user.username, self.date.isoformat())

