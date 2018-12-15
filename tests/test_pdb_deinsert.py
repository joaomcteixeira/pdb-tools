#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 1118 João Pedro Rodrigues
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Unit Tests for `pdb_deinsert`.
"""

import os
import sys
import unittest

from config import data_dir
from utils import OutputCapture


class TestTool(unittest.TestCase):
    """
    Generic class for testing tools.
    """

    def setUp(self):
        # Dynamically import the module
        name = 'pdbtools.pdb_deinsert'
        self.module = __import__(name, fromlist=[''])

    def exec_module(self):
        """
        Execs module.
        """

        with OutputCapture() as output:
            try:
                self.module.main()
            except SystemExit as e:
                self.retcode = e.code

        self.stdout = output.stdout
        self.stderr = output.stderr

        return

    def test_default(self):
        """$ pdb_deinsert data/deinsert_input.pdb"""

        # Simulate input
        # pdb_deinsert deinsert_input.pdb
        sys.argv = ['', os.path.join(data_dir, 'deinsert_input.pdb')]

        # Execute the script
        self.exec_module()

        # Validate results
        self.assertEqual(self.retcode, 0)  # ensure the program exited OK.
        self.assertEqual(len(self.stdout), 6)  # no lines deleted
        self.assertEqual(len(self.stderr), 0)  # no errors

        records = (('ATOM', 'HETATM'))
        resid_list = [l[22:27] for l in self.stdout
                      if l.startswith(records)]

        expected = [
            '   1 ',
            '   1 ',
            '   1 ',
            '   2 ',
            '   2 ',
            '   2 '
        ]

        self.assertEqual(resid_list, expected)

    def test_two_options_pos(self):
        """$ pdb_deinsert -10 data/deinsert_input.pdb"""

        # Simulate input
        # pdb_deinsert -10 deinsert_input.pdb
        sys.argv = ['', '-10', os.path.join(data_dir, 'deinsert_input.pdb')]

        # Execute the script
        self.exec_module()

        # Validate results
        self.assertEqual(self.retcode, 0)  # ensure the program exited OK.
        self.assertEqual(len(self.stdout), 6)  # no lines deleted
        self.assertEqual(len(self.stderr), 0)  # no errors

        records = (('ATOM', 'HETATM'))
        resid_list = [l[22:27] for l in self.stdout
                      if l.startswith(records)]

        expected = [
            '  10 ',
            '  10 ',
            '  10 ',
            '  11 ',
            '  11 ',
            '  11 '
        ]

        self.assertEqual(resid_list, expected)

    def test_two_options_neg(self):
        """$ pdb_deinsert --10 data/deinsert_input.pdb"""

        # Simulate input
        # pdb_deinsert --10 deinsert_input.pdb
        sys.argv = ['', '--10', os.path.join(data_dir, 'deinsert_input.pdb')]

        self.exec_module()

        self.assertEqual(self.retcode, 0)
        self.assertEqual(len(self.stdout), 6)
        self.assertEqual(len(self.stderr), 0)

        records = (('ATOM', 'HETATM'))
        resid_list = [l[22:27] for l in self.stdout
                      if l.startswith(records)]

        expected = [
            ' -10 ',
            ' -10 ',
            ' -10 ',
            '  -9 ',
            '  -9 ',
            '  -9 '
        ]

        self.assertEqual(resid_list, expected)

    def test_too_many_residues(self):
        """$ pdb_deinsert -9999 data/deinsert_input.pdb"""

        sys.argv = ['', '-9999', os.path.join(data_dir, 'deinsert_input.pdb')]

        self.exec_module()

        self.assertEqual(self.retcode, 1)
        self.assertEqual(len(self.stdout), 0)
        self.assertEqual(len(self.stderr), 1)

        self.assertEqual(self.stderr[0][:22],
                         "Cannot set residue num")  # proper error message

    def test_file_not_found(self):
        """$ pdb_deinsert -10 not_existing.pdb"""

        afile = os.path.join(data_dir, 'not_existing.pdb')
        sys.argv = ['', '-10', afile]

        self.exec_module()

        self.assertEqual(self.retcode, 1)  # exit code is 1 (error)
        self.assertEqual(len(self.stdout), 0)  # nothing written to stdout
        self.assertEqual(self.stderr[0][:22],
                         "ERROR!! File not found")  # proper error message

    def test_file_missing(self):
        """$ pdb_deinsert -10"""

        sys.argv = ['', '-10']

        self.exec_module()

        self.assertEqual(self.retcode, 1)
        self.assertEqual(len(self.stdout), 0)  # no output
        self.assertEqual(self.stderr[0],
                         "ERROR!! No data to process!")

    def test_helptext(self):
        """$ pdb_deinsert"""

        sys.argv = ['']

        self.exec_module()

        # ensure the program exited gracefully.
        self.assertEqual(self.retcode, 1)
        self.assertEqual(len(self.stdout), 0)  # no output
        self.assertEqual(self.stderr, self.module.__doc__.split("\n")[:-1])

    def test_invalid_option(self):
        """$ pdb_deinsert -A data/deinsert_input.pdb"""

        sys.argv = ['', '-A', os.path.join(data_dir, 'deinsert_input.pdb')]

        self.exec_module()

        self.assertEqual(self.retcode, 1)
        self.assertEqual(len(self.stdout), 0)
        self.assertEqual(self.stderr[0][:47],
                         "ERROR!! You provided an invalid residue number:")

    def test_not_an_option(self):
        """$ pdb_deinsert 11 data/deinsert_input.pdb"""

        sys.argv = ['', '11', os.path.join(data_dir, 'deinsert_input.pdb')]

        self.exec_module()

        self.assertEqual(self.retcode, 1)
        self.assertEqual(len(self.stdout), 0)
        self.assertEqual(self.stderr[0],
                         "ERROR! First argument is not an option: '11'")


if __name__ == '__main__':
    from config import test_dir

    mpath = os.path.abspath(os.path.join(test_dir, '..'))
    sys.path.insert(0, mpath)  # so we load dev files before  any installation

    unittest.main()
