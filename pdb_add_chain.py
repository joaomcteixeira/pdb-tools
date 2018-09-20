#!/usr/bin/env python

"""
Adds chain IDs to PDB file based on residue number.

usage: python pdb_add_chain.py <pdb file>
examples:
    python pdb_add_chain.py 1CTF.pdb
    python pdb_add_chain.py -res 1CTF.pdb
    python pdb_add_chain.py -ind "OXT HO3'" 1CTF.pdb

=== DESCRIPTION:

Adds chain labels, consecutively following ASCII.string.upper,
in a multi-chain PDB file that lost the chain information.
    
    <- input
    ATOM      1  N   GLY     1      52.630 104.940  39.430  1.00  0.00
    ATOM      2  H1  GLY     1      51.700 105.330  39.400  1.00  0.00
    
    -> output
    ATOM      1  N   GLY A   1      52.630 104.940  39.430  1.00  0.00
    ATOM      2  H1  GLY A   1      51.700 105.330  39.400  1.00  0.00
    
    
    OPTIONS:
    
        -res: Recognizes chain break by residue number.
            When residue number restarts, chain changes.
        
        -ind: Recognizes chain break by last atom identifier.
              When last atom is met, changes chain starting on the next line.
              Identifiers should be passed after OPTION as a space separated 
              sequence wrapped as string.
            
    
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


