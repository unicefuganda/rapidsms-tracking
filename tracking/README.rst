==Configuration==


First of all, you must add this project to your list of `INSTALLED_APPS` in `settings.py`:

{{{
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    ...
    'tracking',
    ...
)
}}}

Run `manage.py syncdb`.  This creates a few tables in your database that are necessary for operation.

==loggedin user tracking==

Add `tracking.middleware.UserTrackingMiddleware` to your `MIDDLEWARE_CLASSES` in `settings.py`.  It must be
underneath the `AuthenticationMiddleware`, so that `request.user` exists.


AUTH_PROFILE_MODULE = 'accounts.UserProfile'


add  AUTH_PROFILE_MODULE = 'tracking.UserProfile'   in order to get the method

- get_profile() --   on the user object

