from django.test import TestCase
from audit_logging_tests.models import TestModel
from audit_logging.models import AuditEvent

class ModelAuditTests(TestCase):
    def setUp(self):
        TestCase.setUp(self)

    def test_create_logged(self):
        TestModel.objects.create()

        latest_auditevent = AuditEvent.objects.order_by('-datetime').first()
        self.assertEqual(latest_auditevent.resource_type, 'TestModel')
        self.assertEqual(latest_auditevent.event, 'create')

    def test_save_logged(self):
        tm = TestModel.objects.create()
        tm.field1 = 'hi'
        tm.save()

        latest_auditevent = AuditEvent.objects.order_by('-datetime').first()
        self.assertEqual(latest_auditevent.resource_type, 'TestModel')
        self.assertEqual(latest_auditevent.event, 'update')

    def test_delete_logged(self):
        tm = TestModel.objects.create()
        tm.delete()
        latest_auditevent = AuditEvent.objects.order_by('-datetime').first()
        self.assertEqual(latest_auditevent.resource_type, 'TestModel')
        self.assertEqual(latest_auditevent.event, 'delete')
