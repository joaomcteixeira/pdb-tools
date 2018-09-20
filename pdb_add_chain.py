#!/usr/bin/env python

"""
Adds chain IDs to PDB file based on residue number.

usage: python pdb_chainbyres.py <pdb file>
examples: python pdb_chainbyres.py 1CTF.pdb

=== DESCRIPTION:

Adds chain labels, consecutively following ASCII.string.upper,
in a multi-chain PDB file that lost the chain information.
Chains are identified based on residue number, chain changes upon
residue number restart.
    
    <- input
    ATOM   1732  CB  LYS   254      54.522  13.130  52.312  1.00 63.84           C  
    ATOM   1733  CG  LYS   254      53.565  13.687  51.260  1.00 63.27           C  
    ATOM   1735  N   PHE     2      -7.485  -6.367  19.069  0.50 64.74           N  
    ATOM   1736  CA  PHE     2      -6.127  -6.372  18.438  0.70 63.43           C  
    
    -> output
    ATOM   1732  CB  LYS A 254      54.522  13.130  52.312  1.00 63.84           C  
    ATOM   1733  CG  LYS A 254      53.565  13.687  51.260  1.00 63.27           C  
    ATOM   1735  N   PHE B   2      -7.485  -6.367  19.069  0.50 64.74           N  
    ATOM   1736  CA  PHE B   2      -6.127  -6.372  18.438  0.70 63.43           C  
    
    
Author: {0} ({1})

This program is part of the PDB tools distributed with HADDOCK
or with the HADDOCK tutorial. The utilities in this package
can be used to quickly manipulate PDB files, with the benefit
of 'piping' several different commands. This is a rewrite of old
FORTRAN77 code that was taking too much effort to compile. RIP.
"""

from __future__ import print_function

import os
import re
import sys

__author__ = "Joao M.C. Teixeira"
__email__ = "joaomcteixeira@gmail.com"

USAGE = __doc__.format(__author__, __email__)


def check_input(args):
    """
    Checks whether to read from stdin/file and validates user input/options.
    """

    if not len(args):
        # Read from pipe
        if not sys.stdin.isatty():
            pdbfh = sys.stdin
        else:
            sys.stderr.write(USAGE)
            sys.exit(1)
    elif len(args) == 1:
        # File
        if not os.path.isfile(args[0]):
            sys.stderr.write('File not found: ' + args[0] + '\n')
            sys.stderr.write(USAGE)
            sys.exit(1)
        pdbfh = open(args[0], 'r')
    else:
        sys.stderr.write(USAGE)
        sys.exit(1)

    return pdbfh
    

def _add_chain_by_res(pdbfh):
    """Runs over each line of the PDB."""
    yield None

if __name__ == '__main__':
    # Check Input
    pdbfh = check_input(sys.argv[1:])

    # Do the job
    new_pdb = _add_chain_by_res(pdbfh)

    try:
        sys.stdout.write(''.join(new_pdb))
        sys.stdout.flush()
    except IOError:
        # This is here to catch Broken Pipes
        # for example to use 'head' or 'tail' without
        # the error message showing up
        pass

    # last line of the script
    # We can close it even if it is sys.stdin
    pdbfh.close()
    sys.exit(0)
