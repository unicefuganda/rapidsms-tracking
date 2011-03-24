from django.conf.urls.defaults import *
from generic.views import generic
from django.contrib.auth.decorators import login_required
from tracking.models import UserProfile
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
                                   ('Last Update', True, 'userprofile__last_update', SimpleSorter(),),
                                   ('Page Views', True, 'userprofile__page_views', SimpleSorter(),),
                                   ('Time On Site', False, 'userprofile__time_on_site', None,),
                                   ('Last Page Visited', True, 'userprofile__url', SimpleSorter(),),
                                   ],

                           }),

                       )