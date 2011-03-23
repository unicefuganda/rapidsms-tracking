import datetime
from tracking.models import UserProfile
class UserTrackingMiddleware:
    """
    Keeps track of loggedin active users.  Anytime a visitor accesses a valid URL,
    their unique record will be updated with the page they're on and the last
    time they requested a page.

    """

    def process_request(self, request):
        # don't process AJAX requests
        if request.is_ajax(): return

        # create some useful variables
        ip_address = utils.get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]

        # see if the user agent is not supposed to be tracked
        for ua in UntrackedUserAgent.objects.all():
            # if the keyword is found in the user agent, stop tracking
            if str(user_agent).find(ua.keyword) != -1:
                return

        if hasattr(request, 'session'):
            # use the current session key if we can
            session_key = request.session.session_key
        else:
            # otherwise just fake a session key
            session_key = '%s:%s' % (ip_address, user_agent)

        # don't track media file requests
        if settings.MEDIA_URL:
            prefixes.append(settings.MEDIA_URL)
        if settings.ADMIN_MEDIA_PREFIX:
            prefixes.append(settings.ADMIN_MEDIA_PREFIX)


        # if we get here, the URL needs to be tracked
        # determine what time it is
        now = datetime.datetime.now()


        # for some reason, Visitor.objects.get_or_create was not working here
        user = request.user
        userprofile = UserProfile.objects.get_or_create(request.user)

        # determine whether or not the user is logged in
        user = request.user
        if isinstance(user, AnonymousUser):
            return

        # update the tracking information
        userprofile.user_agent = user_agent

        # if the visitor record is new, or the visitor hasn't been here for
        # at least an hour, update their referrer URL
        one_hour_ago = now - timedelta(hours=1)
        if not userprofile.last_update or userprofile.last_update <= one_hour_ago:
            userprofile.referrer = request.META.get('HTTP_REFERER', 'unknown')[:255]

            # reset the number of pages they've been to
            userprofile.page_views = 0
            userprofile.session_start = now

        userprofile.url = request.path
        userprofile.page_views += 1
        userprofile.last_update = now
        visitor.save()