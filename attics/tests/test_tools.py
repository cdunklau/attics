from __future__ import absolute_import

import os.path
import unittest
import tempfile
import shutil
import argparse

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
        args = argparse.Namespace(
            input_path=None,
            output_path=None,
            options=[]
        )
        config = make_configuration(
            os.path.join(testdata_dir, 'site.ini'),
            args
        )
        config['attics']['output_path'] = self.outdir
        run(config)
