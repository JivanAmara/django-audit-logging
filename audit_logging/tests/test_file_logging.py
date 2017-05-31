# Perform audit_logging_tests for auditing.
from tempfile import NamedTemporaryFile
from django.test import TestCase
import os
from audit_logging.file_logging import open, LoggingFile
from mock import patch


class LoggingOpenTests(TestCase):

    @patch('audit_logging.file_logging.AuditEvent')
    def test_open_existing(self, AuditEvent):
        with NamedTemporaryFile() as f:
            f2 = open(f.name)
            self.assertIsInstance(f2, LoggingFile)
            f2.close()
            self.assertEqual(AuditEvent.objects.create.call_count, 0)

    @patch('audit_logging.file_logging.AuditEvent')
    def test_open_nonexisting(self, AuditEvent):
        with NamedTemporaryFile() as f:
            fname = f.name
        self.assertFalse(os.path.exists(fname))
        with open(fname, 'w') as f:
            self.assertEqual(AuditEvent.objects.create.call_count, 1)


class LoggingFileTests(TestCase):

    # File methods expected to log an event when they're called, with a valid argument if needed.
    logging_methods = [
        ('write', 'sample'),
        ('writelines', ['sample1', 'sample2']),
        ('truncate', None),
        ('read', None),
        ('readline', None),
        ('readlines', None)
    ]

    @patch('audit_logging.file_logging.AuditEvent')
    def test_log_on_method_call(self, AuditEvent):
        with NamedTemporaryFile() as tf:
            lf = LoggingFile(tf)

            for method, arg in self.logging_methods:
                AuditEvent.reset_mock()
                m = getattr(lf, method)
                if arg is None:
                    m()
                else:
                    m(arg)

                expected_call_count = 1
                msg = 'AuditLogging count {} != {} for LoggingFile.{}()'.format(
                    AuditEvent.objects.create.call_count, expected_call_count, method
                )
                self.assertEqual(AuditEvent.objects.create.call_count, expected_call_count, msg)
