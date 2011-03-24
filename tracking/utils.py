from django.contrib.auth.models import User

def get_users():
    return User.objects.extra(
        select={
            'avg_time':'select avg(extract (epoch from (last_update - session_start))) from tracking_userlog where user_id=auth_user.id',
            'avg_weekly':'select sum(weekly_visits) / count(*) as weekly_average from (select extract(week from session_start) as week, count(*) as weekly_visits from tracking_userlog where user_id=auth_user.id group by week) fullstats',
        })
