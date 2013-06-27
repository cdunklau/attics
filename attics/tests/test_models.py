from __future__ import absolute_import

import os.path
import unittest

from attics.models import Theme, File, Image, Page, BUILT_IN_THEMES


testdata_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'testdata'
)

class IsolateThemeTestCase(unittest.TestCase):
    def test__find_themedir_builtin(self):
        t = Theme('simple', 'bogus')
        t._find_themedir()
        assert t.location == os.path.join(BUILT_IN_THEMES, 'simple')
        assert t.name == 'simple'

    def test__find_themedir_custom(self):
        t = Theme('customtheme', testdata_dir)
        t._find_themedir()
        assert t.location == 'customtheme'
        assert t.name == 'customtheme'

    def test__find_themedir_custom_path(self):
        t = Theme('themes/deepercustom', testdata_dir)
        t._find_themedir()
        assert t.location == 'themes/deepercustom'
        assert t.name == 'deepercustom'

    def test__validate_files_builtin(self):
        t = Theme('simple', 'bogus')
        t.location = os.path.join(BUILT_IN_THEMES, 'simple')
        t._validate_files()

    def test__validate_files_custom(self):
        t = Theme('customtheme', testdata_dir)
        t.location = os.path.join(testdata_dir, 'customtheme')
        t._validate_files()

    def test__validate_files_custom_path(self):
        t = Theme('themes/deepercustom', testdata_dir)
        t.location = os.path.join(testdata_dir, 'themes/deepercustom')
        t._validate_files()

    def test__parse_template(self):
        t = Theme('simple', 'bogus')
        t.location = os.path.join(BUILT_IN_THEMES, 'simple')
        t._parse_template()
