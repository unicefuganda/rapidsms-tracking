from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    user_agent = models.CharField(max_length=255,null=True)
    page_views = models.PositiveIntegerField(default=0)
    url = models.CharField(max_length=255,null=True)
    session_start = models.DateTimeField(null=True)
    last_update = models.DateTimeField(null=True)
    user_agent=models.CharField(max_length=255,null=True)


    def _time_on_site(self):
        """
        Attempts to determine the amount of time a visitor has spent on the
        site based upon their information that's in the database.
        """
        if self.session_start:
            seconds = (self.last_update - self.session_start).seconds

            hours = seconds / 3600
            seconds -= hours * 3600
            minutes = seconds / 60
            seconds -= minutes * 60

            return u'%i:%02i:%02i' % (hours, minutes, seconds)
        else:
            return u'unknown'
    time_on_site = property(_time_on_site)

    class Meta:
        ordering = ('-last_update',)
