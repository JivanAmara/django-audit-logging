# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 Boundless Spatial
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from django.apps import AppConfig


class AuditConfig(AppConfig):
    name = 'audit_logging'
    verbose_name = 'Logging to provide file/django model CRUD audit trail'

    def ready(self):
        # Override built-in open() with the logging version.
        try:
            import __builtin__ as builtins  # Python 2
        except ImportError:
            import builtins  # Python 3
        from audit_logging.file_logging import open as logging_open
        builtins.open = logging_open

        import audit_logging.signals  # noqa
