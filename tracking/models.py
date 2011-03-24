from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg



class UserLog(models.Model):
    user = models.ForeignKey(User,null=True,related_name='userlog')
    user_agent = models.CharField(max_length=255,null=True)
    page_views = models.PositiveIntegerField(default=0)
    url = models.CharField(max_length=255,null=True)
    session_start = models.DateTimeField(null=True)
    last_update = models.DateTimeField(null=True)
    user_agent=models.CharField(max_length=255,null=True)
    session_key=models.CharField(max_length=255,null=True)
    ip_address=models.CharField(max_length=255,null=True)
    referrer=models.CharField(max_length=255,null=True)
    time_on_site = models.PositiveIntegerField(default=0)
    
    def _timeon_site(self):
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
    timeon_site = property(_timeon_site)

    def average_time_on_site(self):
        return UserLog.objects.filter(user=self.user).aggregate(Avg('time_on_site')).get('average_time_on_site',0)


    def average_time_onsite(self):
        pass
    def save(self,*args,**kwargs):
        self.time_on_site=(self.last_update - self.session_start).seconds
        super(UserLog,self).save(*args,**kwargs)

    class Meta:
        ordering = ('-last_update',)

