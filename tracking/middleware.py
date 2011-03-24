import datetime
from tracking.models import UserProfile
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



        user = request.user

           # determine whether or not the user is logged in
        if isinstance(user, AnonymousUser):
            return

        try:
            userprofile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            userprofile=UserProfile.objects.create(user=request.user)



        # update the tracking information
        userprofile.user_agent = user_agent

        userprofile.url=request.path

        # if the visitor record is new, or the visitor hasn't been here for
        # at least an hour, update their referrer URL
        one_hour_ago = now - datetime.timedelta(hours=1)
        if not userprofile.last_update or userprofile.last_update <= one_hour_ago:
            # reset the number of pages they've been to
            userprofile.page_views = 0
            userprofile.session_start = now

        userprofile.url = request.path
        userprofile.page_views += 1
        userprofile.last_update = now
        userprofile.save()