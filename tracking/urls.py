from django.conf.urls.defaults import *
from generic.views import generic
from django.contrib.auth.decorators import login_required
from tracking.models import UserLog
from generic.sorters import SimpleSorter, TupleSorter
from django.contrib.auth.models import User


urlpatterns = patterns('',
                       url(r'^tracking/userlist/$', login_required(generic), {
                           'model':User,
                           'objects_per_page':10,
                           'partial_row':'tracking/partials/tracked_user_row.html',
                           'base_template':'tracking/tracked_users_base.html',
                           'columns':[
                                   ('User', True, 'username', SimpleSorter(),),
                                   ('Group', True, 'groups', SimpleSorter(),),
                                    ('Location', True, 'contact__reporting_location', SimpleSorter(),),
                                   ('Last Update', True, 'userlog__last_update', SimpleSorter(),),
                                   ('Page Views', True, 'userlog__page_views', SimpleSorter(),),
                                   ('Last Page Visited', True, 'userlog__url', SimpleSorter(),),
                                   ('Average Time On Site', True, 'userlog__time_on_site', SimpleSorter(),),
                                   ('Average Weekly Visits', True, 'userlog__time_on_site', SimpleSorter(),)
                                   ],

                           }),

                       )