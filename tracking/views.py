from generic.views import generic
from django.shortcuts import  get_object_or_404
from .models import UserLog
from django.contrib.auth.models import User
from generic.sorters import SimpleSorter
def view_user_history(request, user_id=None):
    user = get_object_or_404(User,pk=user_id)
    return generic(request,
       model=UserLog,
       queryset=UserLog.objects.filter(user=user),
       objects_per_page=10,
       selectable=False,
       partial_row='tracking/partials/userlog_row.html',
#       base_template='tracking/tracked_users_base.html',
       results_title='Browsing history for %s' % user.username,
       sort_column='session_start',
       sort_ascending=False,
       columns=[
           ('Browser', True, 'user_agent', SimpleSorter(),),
           ('Page Views', True, 'page_views', SimpleSorter(),),
           ('Last Page', True, 'url', SimpleSorter(),),
           ('Start Time', True, 'session_start', SimpleSorter(),),
           ('End Time', True, 'last_update', SimpleSorter(),),
       ],
    )