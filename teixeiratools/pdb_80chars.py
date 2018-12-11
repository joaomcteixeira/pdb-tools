#!/usr/bin/env python

"""
Formats lines to 80 char wide by adding trail spaces.

usage: python pdb_80chars.py <pdb file> 

example:
    python pdb_80chars.py file.pdb > new.pdb
    pdb_80chars.py file.pdb > new.pdb
    
Author: {0} ({1})
"""

import os
import sys

__author__ = "Joao M.C. Teixeira"
__email__ = "joaomcteixeira@gmail.com"

USAGE = __doc__.format(__author__, __email__)

def check_input(args):
    
    if not len(args):
        if not sys.stdin.isatty():
            pdbfh = sys.stdin
        else:
            sys.stderr.write(USAGE)
            sys.exit(1)
        
    elif len(args) == 1: 
        if not os.path.isfile(args[0]):
            sys.stderr.write('File not found: ' + args[0] + '\n')
            sys.stderr.write(USAGE)
            sys.exit(1)
            
        else:
            pdbfh = open(args[0], 'r')
    
    else:
        sys.stderr.write(USAGE)
        sys.exit(1)
    
    return pdbfh

def _format_80chars(pdbfh):
    for line in pdbfh:
        yield "{:<80}\n".format(line.rstrip())

if __name__ == '__main__':

    # Check Input
    pdbfh = check_input(sys.argv[1:])

    # Do the job
    new_pdb = _format_80chars(pdbfh)

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
