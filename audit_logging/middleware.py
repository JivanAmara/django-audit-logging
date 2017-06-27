from audit_logging.utils import audit_logging_thread_local

class UserDetailsMiddleware(object):
    """ Saves a dict with user details to thread-local storage to facilitate access in signal handlers
        so user details can be logged with events.  If user details are unavailable stores None.
        @note: Place after AuthenticationMiddleware.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            user_details = {
                'username': request.user.username,
                'is_superuser': request.user.is_superuser,
                'is_staff': request.user.is_staff
            }
        except KeyError:
            user_details = None

        audit_logging_thread_local.user_details = user_details

        response = self.get_response(request)
        return response
