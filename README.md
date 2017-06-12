Add 'audit_logging' to INSTALLED_APPS.
Set AUDIT_MODELS to the models you want audited with the names you want them to be given in logging output:
    AUDIT_MODELS = [
        ('geonode.base.models.ContactRole', 'contactrole'), ('geonode.documents.models.Document', 'document'),
        ('geonode.layers.models.Layer', 'layer'), ('geonode.maps.models.Map', 'map),
    ]
Set AUDIT_FILE_EVENTS to True (default) or False for file creation/read/write event logging.
