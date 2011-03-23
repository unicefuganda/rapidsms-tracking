from django.conf.urls.defaults import *
from generic.views import generic
from django.contrib.auth.decorators import login_required
from tracking.models import UserProfile
from generic.sorters import SimpleSorter, TupleSorter


urlpatterns = patterns('',
  url(r'^tracking/userlist/$', login_required(generic), {
      'model':UserProfile,
      'objects_per_page':10,
      'partial_row':'tracking/partials/tracked_user_row.html',
      'base_template':'tracking/tracked_users_base.html',
      'columns':[('User', True, '', SimpleSorter()),
                 ('Last Update', True, 'connection__c', SimpleSorter(),),
                 ('Page Views', True, 'date', SimpleSorter(),),
                 ('Time On Site', True, 'application', SimpleSorter(),),
                 ],
      
    }),

)