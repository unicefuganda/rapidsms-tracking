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
    
    def average_time_on_site(self):
        return User.objects.filter(username='mossplix').extra( select={'avg_time':'select avg(extract (epoch from (last_update - session_start))) from tracking_userlog where user_id=%d'%self.user.pk})[0].avg_time

    def average_weekly_visits(self):
        return User.objects.filter(pk=self.user.pk).extra( select={'avg_weekly':'select sum(weekly_visits) / count(*) as weekly_average from (select extract(week from session_start) as week, count(*) as weekly_visits from tracking_userlog where user_id=%d group by week) fullstats'%self.user.pk})[0].avg_weekly
    def save(self,*args,**kwargs):
        try:
            self.time_on_site=(self.last_update - self.session_start).seconds
        except:
            pass
        super(UserLog,self).save(*args,**kwargs)

    class Meta:
        ordering = ('-last_update',)

