""" Provides alterntive open() & File objects which log create/read/update/delete.
"""
import os
from audit_logging.models import AuditEvent
import logging
from django.db import connection
from django.conf import settings


logger = logging.getLogger(__name__)


def log_event(event=None, resource_type='file', resource_uuid=None):
    try:
        AuditEvent.objects.create(event=event, resource_type=resource_type, resource_uuid=resource_uuid)
    except Exception as ex:
        pass


def logging_open(filepath, *args):
    """ Equivalent of builtin open() which logs file creation to AuditEvent if appropriate and returns a LoggingFile
        instead of regular file-like object.
    """
    exists_before = os.path.exists(filepath)
    res = open(filepath, *args)

    if getattr(settings, 'AUDIT_FILE_EVENTS', True):
        res = LoggingFile(res)
        exists_after = os.path.exists(filepath)

        if not exists_before and exists_after:
            log_event(event='FileCreate', resource_type='file', resource_uuid=filepath)

    return res


class LoggingFile(object):
    """ Wraps a regular file-like object so that reads/writes are logged to AuditEvent.
    """
    regular_file = None
    AuditEvent = None

    def __init__(self, regular_file):
        """ regular_file should be an open file-like object
        """
        # Import AuditEvent here so this module can be imported before django apps are ready
        from audit_logging.models import AuditEvent
        self.AuditEvent = AuditEvent
        self.regular_file = regular_file

    def write(self, *args, **kwargs):
        res = self.regular_file.write(*args, **kwargs)
        log_event(event='FileWrite', resource_type='file', resource_uuid=self.regular_file.name)
        return res

    def writelines(self, *args, **kwargs):
        res = self.regular_file.writelines(*args, **kwargs)
        log_event(event='FileWrite', resource_type='file', resource_uuid=self.regular_file.name)
        return res

    def truncate(self, *args, **kwargs):
        res = self.regular_file.truncate(*args, **kwargs)
        log_event(event='FileWrite', resource_type='file', resource_uuid=self.regular_file.name)
        return res

    def read(self, *args, **kwargs):
        res = self.regular_file.read(*args, **kwargs)
        log_event(event='FileRead', resource_type='file', resource_uuid=self.regular_file.name)
        return res

    def readline(self, *args, **kwargs):
        res = self.regular_file.readline(*args, **kwargs)
        log_event(event='FileRead', resource_type='file', resource_uuid=self.regular_file.name)
        return res

    def readlines(self, *args, **kwargs):
        res = self.regular_file.readlines(*args, **kwargs)
        log_event(event='FileRead', resource_type='file', resource_uuid=self.regular_file.name)
        return res

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        self.regular_file.close()

    def __iter__(self, *args, **kwargs):
        return self.regular_file.__iter__(*args, **kwargs)

    def __next__(self, *args, **kwargs):
        return self.regular_file.__next__(*args, **kwargs)

    def __getattr__(self, attr):
        if hasattr(self.regular_file, attr):
            res = getattr(self.regular_file, attr)
        else:
            raise AttributeError("LoggingFile object has no attribute '{}'".format(attr))

        return res
