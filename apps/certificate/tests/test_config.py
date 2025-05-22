from django.test import TestCase
from django.conf import settings

# Test configuration settings
TEST_SETTINGS = {
    'TEST_RUNNER': 'django.test.runner.DiscoverRunner',
    'TEST_DISCOVER_TOP_LEVEL': settings.BASE_DIR,
    'TEST_DISCOVER_ROOT': settings.BASE_DIR / 'apps' / 'certificate' / 'tests',
    'TEST_DISCOVER_PATTERN': 'test_*.py',
}

# This file is used to configure test discovery
# It ensures that only tests in the certificate app are discovered
