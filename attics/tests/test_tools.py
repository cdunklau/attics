from __future__ import absolute_import

import os.path
import unittest
import tempfile
import shutil
import argparse
import logging
logging.basicConfig(level=logging.DEBUG)

from attics.tools import run, make_configuration

testdata_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'testdata'
)


class AtticsTestCase(unittest.TestCase):
    def setUp(self):
        self.outdir = tempfile.mkdtemp(prefix='attics_test')

    def tearDown(self):
        shutil.rmtree(self.outdir)

    def test_run_attics(self):
        config = make_configuration(
            os.path.join(testdata_dir, 'site.ini'),
            input_path=None,
            output_path=self.outdir,
        )
        run(config)
