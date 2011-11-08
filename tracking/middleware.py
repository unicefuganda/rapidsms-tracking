import datetime
from tracking.models import UserLog
from django.contrib.auth.models import AnonymousUser
from django.conf import settings

class UserTrackingMiddleware:
    """
    Keeps track of loggedin active users.  Anytime a visitor accesses a valid URL,
    their unique record will be updated with the page they're on and the last
    time they requested a page.

    """

    def process_request(self, request):
        # don't process AJAX requests
        if request.is_ajax(): return
        prefixes = []

        # don't track media file requests
        if settings.MEDIA_URL:
            prefixes.append(settings.MEDIA_URL)
        if settings.ADMIN_MEDIA_PREFIX:
            prefixes.append(settings.ADMIN_MEDIA_PREFIX)
        for prefix in prefixes:
            if request.path.startswith(prefix):
                return
        # create some useful variables
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
         # determine what time it is
        now = datetime.datetime.now()
        if hasattr(request, 'session'):
            # use the current session key if we can
            session_key = request.session.session_key
        else:
            # otherwise just fake a session key
            session_key = '%s:%s' % (ip_address, user_agent)
        user = request.user
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR',
                                  request.META.get('REMOTE_ADDR', '127.0.0.1'))
        if isinstance(user, AnonymousUser):
            user = None

        userlogs = UserLog.objects.filter(session_key=session_key,user=user,ip_address=ip_address)
        try:
            userlog=userlogs[0]
        except IndexError:
            userlog=UserLog.objects.create(session_key=session_key,user=user,ip_address=ip_address)

        # update the tracking information
        userlog.user_agent = user_agent

        userlog.url=request.path

        userlog.referrer = request.META.get('HTTP_REFERER', 'unknown')[:255]
        userlog.ip_address=ip_address
        one_hour_ago = now - datetime.timedelta(hours=1)
        if not userlog.last_update or userlog.last_update <= one_hour_ago:
            # reset the number of pages they've been to
            userlog.page_views = 0
            userlog.session_start = now

        userlog.url = request.path
        userlog.page_views += 1
        userlog.last_update = now
        userlog.save()