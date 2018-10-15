#!/usr/bin/env python

"""
Deletes a given ATOM type from a PDB file, scans ATOM and HETATM lines.

usage: python pdb_delatom.py -[ATOM] <pdb file> 

    OPTIONS:
        - ATOM (string): CASE SENSITIVE name of the atom to be removed.

example:
    python pdb_delatom.py -H file.pdb > new.pdb
    python pdb_delatom.py -Cl file.pdb > new.pdb
    
Author: {0} ({1})

This program is part of the PDB tools distributed with HADDOCK
or with the HADDOCK tutorial. The utilities in this package
can be used to quickly manipulate PDB files, with the benefit
of 'piping' several different commands. This is a rewrite of old
FORTRAN77 code that was taking too much effort to compile. RIP.
"""

import os
import sys

__author__ = "Joao M.C. Teixeira"
__email__ = "joaomcteixeira@gmail.com"

USAGE = __doc__.format(__author__, __email__)

def check_input(args):
    
    if not len(args):
        sys.stderr.write(USAGE)
        sys.exit(1)
        
    elif len(args) == 1: 
        if not sys.stdin.isatty():
            pdbfh = sys.stdin
        else:
            sys.stderr.write(USAGE)
            sys.exit(1)
            
        if args[0].startswith('-'):
            atom = args[0].lstrip('-')
        else:
            sys.stderr.write('Bad input: ' + args[0] + '\n')
            sys.stderr.write(USAGE)
            sys.exit(1)
    
    elif len(args) == 2:
        if args[0].startswith('-'):
            atom = args[0].lstrip('-').
        else:
            sys.stderr.write('Bad input: ' + args[0] + '\n')
            sys.stderr.write(USAGE)
            sys.exit(1)
    
        if not os.path.isfile(args[1]):
            sys.stderr.write('File not found: ' + args[1] + '\n')
            sys.stderr.write(USAGE)
            sys.exit(1)
        else:
            pdbfh = open(args[1], 'r')
    
    else:
        sys.stderr.write(USAGE)
        sys.exit(1)
    
    return (atom, pdbfh)

def _remove_atom_type(atom, pdbfh):
    
    for line in pdbfh:
        if line.startswith(('ATOM', 'HETATM')) \
                and line.strip().split()[-1] == atom:
            continue
        yield line

if __name__ == '__main__':

    # Check Input
    atom, pdbfh = check_input(sys.argv[1:])

    # Do the job
    new_pdb = _remove_atom_type(atom, pdbfh)

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
