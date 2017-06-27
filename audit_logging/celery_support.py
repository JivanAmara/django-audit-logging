from celery import Task

class UserDetailsBase(Task):
    """ Grabs user_details kwarg if it's available and stores user details in thread-local storage so
        signal handlers (in particular logging handlers) have access to the details.
    """
    def __call__(self, *args, **kwargs):
        from audit_logging.utils import audit_logging_thread_local

        try:
            audit_logging_thread_local.user_details = kwargs['user_details']
        except KeyError:
            audit_logging_thread_local.user_details = None

        return super(UserDetailsBase, self).__call__(*args, **kwargs)
