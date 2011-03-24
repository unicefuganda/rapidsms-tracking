from django.conf.urls.defaults import *
from generic.views import generic
from django.contrib.auth.decorators import login_required
from tracking.models import UserLog
from generic.sorters import SimpleSorter, TupleSorter
from django.contrib.auth.models import User
from .utils import get_users

urlpatterns = patterns('',
                       url(r'^tracking/userlist/$', login_required(generic), {
                           'model':User,
                           'queryset':get_users,
                           'objects_per_page':10,
                           'selectable':False,
                           'partial_row':'tracking/partials/tracked_user_row.html',
                           'base_template':'tracking/tracked_users_base.html',
                           'columns':[
                                   ('User', True, 'username', SimpleSorter(),),
                                   ('Group', True, 'groups', SimpleSorter(),),
                                   ('Last Update', False, 'last_update', None,),
                                   ('Page Views', False, 'page_views', None,),
                                   ('Last Page Visited', False, '', None,),
                                   ('Average Visit Time (min)', True, 'avg_time', SimpleSorter(),),
                                   ('Average Weekly Visits', True, 'avg_weekly', SimpleSorter(),)
                                   ],

                           }),

                       )